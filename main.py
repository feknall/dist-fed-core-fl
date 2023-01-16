import sys

sys.path.append("")

user_type = sys.argv[1]

if user_type == 'flAdmin':
    from fladmin.fedavg import fl_admin_runner as runner

    address = sys.argv[2]
    port = sys.argv[3]

    runner.run(address, port)

elif user_type == 'aggregator':
    from aggregator import aggregator_runner as runner

    address = sys.argv[2]
    port = sys.argv[3]

    runner.run(address, port)

elif user_type == 'leadAggregator':
    address = sys.argv[2]
    port = sys.argv[3]
    fed_avg = bool(sys.argv[4])

    if fed_avg:
        if fed_avg:
            from leadaggregator.fedavg import lead_aggregator_runner as runner
        else:
            from leadaggregator.fedshare import lead_aggregator_runner as runner

    runner.run(address, port)

elif user_type == 'trainer':
    address = sys.argv[2]
    port = sys.argv[3]
    fed_avg = bool(sys.argv[4])
    client_index = int(sys.argv[5])

    if fed_avg:
        from trainer.fedavg import trainer_runner as runner
    else:
        from trainer.fedshare import trainer_runner as runner

    runner.run(address, port, client_index)
