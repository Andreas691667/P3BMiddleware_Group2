from PlayerView import PlayerView

def main():
    """Main function"""
    view = PlayerView()

    while True:
        print('hello')
        view.model.sc.update()
