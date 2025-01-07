from colorama import Fore, init

class UserInput:
    init(autoreset=True)
    @staticmethod
    def confirm(message: str, confirm_message:str="y",decline_message:str="n")->bool:
        confirmation = input(Fore.YELLOW + f"{message} ({confirm_message}/{decline_message}): ").strip().lower()
        return (confirmation == confirm_message)

    @staticmethod
    def convertToBool(value: str)->bool:
        trueValues = ["true","yes"]
        falseValues = ["false","no"]
        if value.lower() in trueValues:
            return True
        elif value.lower() in falseValues:
            return False
        else:
            raise Exception("Invalid boolean value")