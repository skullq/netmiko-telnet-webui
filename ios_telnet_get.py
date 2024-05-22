from flask import Flask, render_template, request
from netmiko import ConnectHandler

app = Flask(__name__)

def connect_to_cisco(ip_address):
    cisco_device = {
        'device_type': 'cisco_ios_telnet',
        'ip': ip_address,
        'username': 'cisco',
        'password': 'cisco',
        'timeout' : 15
    }
    connection = ConnectHandler(**cisco_device)
    return connection

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        command = request.form.get('command')
        ip_address = request.form.get('ip_address')
        try:
            connection = connect_to_cisco(ip_address)
            output = connection.send_command(command)
            connection.disconnect()
            return render_template('result.html', output=output)
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="10.1.1.2", port=8000, debug=True)
