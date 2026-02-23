from colorama import Fore, Back

def cyan(text):
    print(Fore.CYAN+f"{text}")

def green(text):
    print(Fore.GREEN+f"{text}")

def red(text):
    print(Fore.RED+f"{text}")


def cyan_r(text):
    return Fore.CYAN+f"{text}"

def green_r(text):
    return Fore.GREEN+f"{text}"

def red_r(text):
    return Fore.RED+f"{text}"