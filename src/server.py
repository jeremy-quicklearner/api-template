from pkg import service

def main():
    print('[server] Initializing Service...')
    try:
        svc = service.Service()
    except Exception as e:
        raise Exception('Failed to initialize service') from e

    print('[server] Running Service...')
    try:
        svc.run()
    finally:
        print('[server] Service terminated. Finalizing...')
        svc.finalize()
        print('[server] Service finalized')

if __name__ == '__main__':
    main()
