from .domain import (
    AsteriskConfiguration,
    BlackoutWindow,
    DialplanRule,
    DialShortcutRule,
    ExternalDialplanRule,
    InboundExternalCallerRule,
    PublicInboundNumber,
    SipEndpoint,
)
from directory.models import (
    AllowedChildFamilyRelationship,
    ChildBlackoutPeriod,
    Device,
    DialShortcut,
    ExternalContactPermission,
    ExternalNumberExtension,
    PublicPhoneNumber,
)


def build_asterisk_configuration():
    blackout_windows_by_child_id = {}
    for period in ChildBlackoutPeriod.objects.filter(is_active=True).order_by(
        "child_id",
        "day_group",
        "start_time",
        "end_time",
        "id",
    ):
        blackout_windows_by_child_id.setdefault(period.child_id, []).append(
            BlackoutWindow(
                time_range=period.asterisk_time_range,
                days=period.asterisk_days,
            )
        )

    endpoints = tuple(
        SipEndpoint(
            device_id=device.id,
            owner_type=device.owner_type,
            owner_id=device.owner.id,
            owner_display_name=device.owner_display_name,
            family_id=device.owning_family.id,
            extension=device.sip_extension,
            username=device.sip_username,
            secret=device.sip_secret,
            child_id=device.assigned_child_id,
            blackout_windows=tuple(
                blackout_windows_by_child_id.get(device.assigned_child_id, ())
            ),
        )
        for device in Device.objects.filter(is_active=True)
        .select_related("assigned_child", "assigned_parent", "assigned_family")
        .order_by("id")
    )
    endpoints_by_device_id = {endpoint.device_id: endpoint for endpoint in endpoints}
    endpoints_by_child_id = {}
    for endpoint in endpoints:
        if endpoint.child_id:
            endpoints_by_child_id.setdefault(endpoint.child_id, []).append(endpoint)

    approved_child_family_pairs = set(
        AllowedChildFamilyRelationship.objects.filter(
            approved_by_child_family_guardian__isnull=False,
            approved_by_target_family_guardian__isnull=False,
        ).values_list("child_id", "target_family_id")
    )

    rules = []
    for source in endpoints:
        for target in endpoints:
            if source.device_id == target.device_id:
                continue
            if _endpoints_may_call(source, target, approved_child_family_pairs):
                rules.append(DialplanRule(source_endpoint=source, target_endpoint=target))

    public_inbound_numbers = tuple(
        PublicInboundNumber(
            public_phone_number_id=number.id,
            normalized_number=number.normalized_number,
            label=number.label,
            family_id=number.assigned_family_id,
        )
        for number in PublicPhoneNumber.objects.filter(is_active=True).order_by(
            "normalized_number", "id"
        )
    )
    public_inbound_numbers_by_family_id = {}
    shared_public_inbound_numbers = []
    for public_number in public_inbound_numbers:
        if public_number.family_id:
            public_inbound_numbers_by_family_id.setdefault(
                public_number.family_id,
                [],
            ).append(public_number)
        else:
            shared_public_inbound_numbers.append(public_number)

    external_extensions_by_number_id = {
        extension.external_phone_number_id: extension
        for extension in ExternalNumberExtension.objects.filter(is_active=True)
        .select_related("external_phone_number")
        .order_by("dial_extension", "id")
    }

    external_rules = []
    for permission in (
        ExternalContactPermission.objects.filter(approved_by__isnull=False)
        .select_related("child", "external_phone_number")
        .order_by("child_id", "external_phone_number__normalized_number", "id")
    ):
        sources = endpoints_by_child_id.get(permission.child_id, ())
        extension = external_extensions_by_number_id.get(
            permission.external_phone_number_id
        )
        if not sources or not extension:
            continue
        for source in sources:
            external_rules.append(
                ExternalDialplanRule(
                    source_endpoint=source,
                    external_number_extension_id=extension.id,
                    dialed_extension=extension.dial_extension,
                    normalized_number=extension.external_phone_number.normalized_number,
                )
            )

    inbound_rule_candidates = []
    for permission in (
        ExternalContactPermission.objects.filter(approved_by__isnull=False)
        .select_related("child", "child__family", "external_phone_number")
        .order_by(
            "child__family_id",
            "external_phone_number__normalized_number",
            "child_id",
            "id",
        )
    ):
        targets = endpoints_by_child_id.get(permission.child_id, ())
        public_numbers = tuple(
            public_inbound_numbers_by_family_id.get(
                permission.child.family_id,
                (),
            )
        ) + tuple(shared_public_inbound_numbers)
        if not targets or not public_numbers:
            continue
        for public_number in public_numbers:
            for target in targets:
                inbound_rule_candidates.append(
                    InboundExternalCallerRule(
                        public_phone_number_id=public_number.public_phone_number_id,
                        caller_normalized_number=(
                            permission.external_phone_number.normalized_number
                        ),
                        target_endpoint=target,
                    )
                )

    inbound_rules_by_key = {}
    for rule in inbound_rule_candidates:
        inbound_rules_by_key[
            (
                rule.public_phone_number_id,
                rule.caller_normalized_number,
                rule.target_endpoint.device_id,
            )
        ] = rule

    inbound_external_caller_rules = tuple(
        sorted(
            inbound_rules_by_key.values(),
            key=lambda rule: (
                rule.public_phone_number_id,
                rule.caller_normalized_number,
                rule.target_endpoint.extension,
                rule.target_endpoint.device_id,
            ),
        )
    )

    shortcut_rules = []
    for shortcut in (
        DialShortcut.objects.filter(is_active=True)
        .select_related(
            "source_device",
            "internal_target_device",
            "external_target_extension",
            "external_target_extension__external_phone_number",
            "parent_phone_target",
        )
        .order_by("source_device_id", "digits", "id")
    ):
        source = endpoints_by_device_id.get(shortcut.source_device_id)
        if not source:
            continue
        if shortcut.internal_target_device_id:
            target = endpoints_by_device_id.get(shortcut.internal_target_device_id)
            if not target:
                continue
            shortcut_rules.append(
                DialShortcutRule(
                    source_endpoint=source,
                    digits=shortcut.digits,
                    target_endpoint=target,
                )
            )
        elif (
            shortcut.external_target_extension_id
            and shortcut.external_target_extension.is_active
        ):
            shortcut_rules.append(
                DialShortcutRule(
                    source_endpoint=source,
                    digits=shortcut.digits,
                    external_number_extension_id=shortcut.external_target_extension_id,
                    normalized_number=(
                        shortcut.external_target_extension.external_phone_number.normalized_number
                    ),
                )
            )
        elif shortcut.parent_phone_target_id and shortcut.parent_phone_target.phone:
            shortcut_rules.append(
                DialShortcutRule(
                    source_endpoint=source,
                    digits=shortcut.digits,
                    normalized_number=shortcut.parent_phone_target.phone,
                )
            )

    return AsteriskConfiguration(
        endpoints=endpoints,
        public_inbound_numbers=public_inbound_numbers,
        external_dialplan_rules=tuple(external_rules),
        inbound_external_caller_rules=inbound_external_caller_rules,
        shortcut_rules=tuple(shortcut_rules),
        dialplan_rules=tuple(
            sorted(
                rules,
                key=lambda rule: (
                    rule.source_endpoint.device_id,
                    rule.target_endpoint.extension,
                    rule.target_endpoint.device_id,
                ),
            )
        ),
    )


def _endpoints_may_call(source, target, approved_child_family_pairs):
    if source.family_id == target.family_id:
        return True

    if source.child_id and target.child_id:
        return (
            source.child_id,
            target.family_id,
        ) in approved_child_family_pairs and (
            target.child_id,
            source.family_id,
        ) in approved_child_family_pairs

    if source.child_id:
        return (source.child_id, target.family_id) in approved_child_family_pairs

    if target.child_id:
        return (target.child_id, source.family_id) in approved_child_family_pairs

    return False
