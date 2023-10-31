from PlayerView import PlayerView

if __name__ == "__main__":
    view = PlayerView()

    while True:
        view.model.sc.update()
        print("BusterSalomon is here!")
