import zapi


def main():
    zpi = zapi.ZApi()
    markets = zpi.markets()
    print markets

if __name__ == '__main__':
    main()