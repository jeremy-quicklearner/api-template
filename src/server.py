from pkg import service

def main():
    print('[server] Starting Service...')
    try:
        service.run()
    finally:
        print('[server] Service terminated. Finalizing...')
        service.finalize()
        print('[server] Service finalized')

if __name__ == '__main__':
    main()
