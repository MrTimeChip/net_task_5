import socket
import configparser
import ssl
import base64
import mime_builder


def get_my_ip():
    my_host = socket.gethostname()
    ip = socket.gethostbyname(my_host)
    return ip


MY_IP = get_my_ip()
skip_read = False


def get_send_info(path):
    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')
    receivers = config.get('SMTP', 'receivers').split(',')
    topic = config.get('SMTP', 'topic')
    attachments = config.get('SMTP', 'attachments').split(',')
    if len(attachments) == 1 and attachments[0] == '':
        attachments = []
    return receivers, topic, attachments


def get_auth_info(path):
    config = configparser.ConfigParser()
    config.read(path)
    login = config.get('LOGIN', 'login')
    password = config.get('LOGIN', 'password')
    return login, password


def get_mail_text(path):
    with open(path) as f:
        return f.read()


def execute_command(sock: socket.socket, command):
    print(f'C: {command}')
    sock.send(command.encode('utf-8'))
    if not skip_read:
        data = sock.recv(4096)
        print(f"S: {data.decode('ascii', errors='ignore')}")


def encode_attachment(path):
    with open(f'info/{path}', 'rb') as f:
        content = f.read()
    return base64.standard_b64encode(content).decode('ascii')


def form_mime(plain_text, attachments):
    mime = ''
    mime += mime_builder.HEADER
    for attachment in attachments:
        mime += f'\n--{mime_builder.MIME_BOUNDRY}\n'
        encoded = encode_attachment(attachment)
        filename = attachment.split('/')[-1]
        mime += mime_builder.FILE_TEMPLATE.format(filename, encoded)
    mime += f'\n--{mime_builder.MIME_BOUNDRY}\n'
    mime += mime_builder.PLAIN_TEXT_TEMPLATE.format(plain_text)
    mime += f'\n--{mime_builder.MIME_BOUNDRY}--\n'
    return mime


def send_mail_to(receiver, plain_text, topic, attachments):
    global skip_read
    receiver_server = 'smtp.yandex.ru'
    login, password = get_auth_info('info/send_info.ini')
    login_en = base64.standard_b64encode(login.encode()).decode('ascii')
    password_en = base64.standard_b64encode(password.encode()).decode('ascii')
    context = ssl.create_default_context()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((receiver_server, 465))
        with context.wrap_socket(sock, server_hostname=receiver_server) as ssock:
            execute_command(ssock, f'HELO {MY_IP}\r\n')
            execute_command(ssock, 'AUTH LOGIN\r\n')
            execute_command(ssock, login_en + '\r\n')
            execute_command(ssock, password_en + '\r\n')
            execute_command(ssock, f'MAIL FROM:<{login}>\r\n')
            execute_command(ssock, f'RCPT TO:<{receiver}>\r\n')
            execute_command(ssock, f'DATA\r\n')
            skip_read = True
            execute_command(ssock, f'From: Me <{login}>\r\n')
            execute_command(ssock, f'To: You <{receiver}>\r\n')
            execute_command(ssock, f'Subject: {topic}\r\n')
            mime = form_mime(plain_text, attachments)
            execute_command(ssock, mime)
            skip_read = False
            execute_command(ssock, '\r\n.\r\n')
            execute_command(ssock, 'QUIT\r\n')


def main():
    receivers, topic, attachments = get_send_info('info/send_info.ini')
    plain_text = get_mail_text('info/send_text.txt')
    for receiver in receivers:
        send_mail_to(receiver, plain_text, topic, attachments)


if __name__ == '__main__':
    main()
