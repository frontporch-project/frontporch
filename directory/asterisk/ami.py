import socket
from dataclasses import dataclass


class AsteriskManagerError(Exception):
    """Raised when Asterisk Manager Interface returns an error."""


@dataclass(frozen=True)
class AsteriskManagerSettings:
    host: str
    port: int
    username: str
    password: str
    timeout: float = 5.0


class AsteriskManagerClient:
    def __init__(self, settings, socket_factory=socket.create_connection):
        self.settings = settings
        self.socket_factory = socket_factory

    def run_cli_commands(self, commands):
        with self._connect() as connection:
            reader = connection.makefile("r", encoding="utf-8", newline="\r\n")

            greeting = reader.readline()
            if not greeting.startswith("Asterisk Call Manager/"):
                raise AsteriskManagerError("Asterisk Manager Interface did not greet us.")

            self._send_action(
                connection,
                {
                    "Action": "Login",
                    "Username": self.settings.username,
                    "Secret": self.settings.password,
                },
            )
            login_response = self._read_response(reader)
            self._raise_for_error(login_response)

            results = []
            for command in commands:
                self._send_action(
                    connection,
                    {
                        "Action": "Command",
                        "Command": command,
                    },
                )
                response = self._read_response(reader)
                self._raise_for_error(response)
                results.append(AsteriskManagerCommandResult(command, response))

            self._send_action(connection, {"Action": "Logoff"})
            return tuple(results)

    def _connect(self):
        return self.socket_factory(
            (self.settings.host, self.settings.port),
            timeout=self.settings.timeout,
        )

    def _send_action(self, connection, fields):
        lines = []
        for key, value in fields.items():
            lines.append(f"{key}: {value}")
        payload = "\r\n".join(lines) + "\r\n\r\n"
        connection.sendall(payload.encode("utf-8"))

    def _read_message(self, reader):
        fields = {}
        output = []
        while True:
            line = reader.readline()
            if line == "":
                raise AsteriskManagerError("Asterisk Manager Interface closed the connection.")

            line = line.rstrip("\r\n")
            if not line:
                break
            if line == "--END COMMAND--":
                output.append(line)
                break
            if ": " not in line:
                output.append(line)
                continue

            key, value = line.split(": ", 1)
            if key == "Output":
                output.append(value)
            else:
                fields[key] = value

        if output:
            fields["Output"] = "\n".join(output)
        return fields

    def _read_response(self, reader):
        while True:
            message = self._read_message(reader)
            if "Response" in message:
                return message

    def _raise_for_error(self, message):
        if message.get("Response") == "Error":
            detail = message.get("Message", "Asterisk Manager Interface request failed.")
            raise AsteriskManagerError(detail)


@dataclass(frozen=True)
class AsteriskManagerCommandResult:
    command: str
    response: dict

    @property
    def output(self):
        return self.response.get("Output", "")
