from enum import Enum, unique


@unique
class EchoStyle(Enum):
    HrEqual = -1  # horizontal rule (equal)
    HrDash = -2  # horizontal rule (dash)
    Title = 1  # title of a step
    Running = 2  # running a sub-step
    Complete = 3  # completed a step
    Finish = 4  # finish of all the steps
    Warn = 10  # warning message
    Exit = 20  # error message (and exit)

    def echo(self, content: str = ""):
        def line_of(char):
            print(f'\n{char * 60}\n')

        if self is EchoStyle.HrEqual:
            line_of("=")
        elif self is EchoStyle.HrDash:
            line_of("-")
        elif self is EchoStyle.Title:
            EchoStyle.HrEqual.echo()
            print(f' * {content}...')
            EchoStyle.HrDash.echo()
        elif self is EchoStyle.Running:
            print(f' - {content}')
        elif self is EchoStyle.Complete:
            print(f'\n * {content} completed.')
        elif self is EchoStyle.Finish:
            EchoStyle.HrEqual.echo()
            print(f' * {content}')
            EchoStyle.HrEqual.echo()
        elif self is EchoStyle.Warn:
            print(f' ? {content}')
        elif self is EchoStyle.Exit:
            import sys
            sys.exit(f' ! {content}')
