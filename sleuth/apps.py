#!/usr/bin/env python3

import readline

# TODO place package in /usr/local/bin
# TODO chmod +x apps.py
# TODO get package via scp into current directory (.)
# TODO scp -r username@ip:/path/to/remote/server/source/folder .

index = {1: 'APP1',
         2: 'APP2'}

intro = '''\nWelcome to Sleuth.\n
Enter the number of the system you wish to test or Ctrl+C to exit:'''


def main():
    """ List a number of possibilities where each is a system test script."""

    while True:
        try:
            print(intro)

            for k, v in sorted(index.items()):
                print('\t', k, ': ', v, sep='')

            choice = int(input('\nEnter a number> '))
            application = index.get(choice, 'Not a valid selection!')

            if application == 'APP1':
                import application1
                application1.main()
            elif application == 'APP2':
                import application2
                application2.main()
            else:
                print('\n'+application)
                main()
        except ValueError:
            print('Not a valid selection; enter a valid number.')
        except KeyboardInterrupt:
            print('\n\nThank you for using Sleuth.')
            exit()

if __name__ == "__main__":
    main()

