# В тексте задания не сказано про валидацию данных, так что я принял решение решать задания как олипиадные
# То есть все входные данные правильные

import re


class Email:
    def __init__(self, email: str):
        self.email = email

    def shielding(self, symbol: str = 'x'):
        mail, domain = self.email.split('@')
        return symbol * len(mail) + '@' + domain


class Phone:
    def __init__(self, phone: str):
        self.phone = phone

    def shielding(self, symbol: str = 'x', numbers: int = 3):
        counter = 1
        phone_list = list(self.phone.replace(' ', ''))  # создаем лист, так как строки неизменяемы
        for elem in reversed(range(len(phone_list))):
            if numbers > 0:
                phone_list[elem] = symbol
                numbers -= 1
            if not counter % 3:     # Оступ каждый 3 элемент
                phone_list.insert(elem, ' ')
            counter += 1

        return ''.join(phone_list)


class Skype:
    def __init__(self, skype: str):
        self.skype = skype

    def shielding(self):
        pure_skype = re.search('skype:[^?\b]+', self.skype).group(0)
        return self.skype.replace(pure_skype, 'skype:xxx')


if __name__ == '__main__':
    print('__ Email __')
    email = Email('aaa@aaa.com')
    print(email.shielding())
    print(email.shielding('*'))

    print('\n__ Phone __')
    phone = Phone('+7 666 777   888')
    print(phone.shielding())
    print(phone.shielding('*'))

    print('\n__ Skype __')
    skype1 = Skype("skype:alex.max")
    skype2 = Skype("<a href=\"skype:xxx?call\">skype</a>")
    print(skype1.shielding())
    print(skype2.shielding())
