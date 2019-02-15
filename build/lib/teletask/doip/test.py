from telegram import Telegram, TelegramSetting, TelegramFunction, TelegramCommand, TeletaskConst

def main():
    msg = Telegram(TelegramCommand.SET,TelegramFunction.RELAY,1,TelegramSetting.TOGGLE)
    print(msg)
 
if __name__ == '__main__':
    main()