import subprocess

result = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
result = result.decode('gbk')
lst = result.split('\r\n')
lst = lst[4:]

for index in range(len(lst)):
    if index % 5 == 0:
        print(lst[index])