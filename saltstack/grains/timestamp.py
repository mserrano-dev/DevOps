import datetime

def main():
    """
    Grain that will return the current datetime in isoformat
    """
    today = datetime.datetime.now()
    today = today.replace(microsecond=0)
    return {'timestamp': today.isoformat(' ')}

if __name__ == '__main__':
    print main()
