# Memristor Sync
The script synchronises different online services used by Memristor (eg. gets Slack users and puts it in Google Spreadsheet). It is executed every hour by [SemaphoreCI](https://semaphoreci.com/lukicdarkoo/management-sync).

## Install
```
pip install --user -r requirements.txt
```

## TODO
- Add header
- Don't delete a field if the field is filled manually