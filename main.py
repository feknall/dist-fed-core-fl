import asyncio
import sys

sys.path.append("")

user_type = sys.argv[1]

loop = asyncio.get_event_loop()

address = sys.argv[2]
port = sys.argv[3]
fed_avg = sys.argv[4] == "True"

if user_type == 'flAdmin':
    if fed_avg:
        print("flAdmin - FedAvg")
        from fladmin.fedavg import fl_admin_runner as runner
    else:
        print("flAdmin - FedShare")
        from fladmin.fedshare import fl_admin_runner as runner

    loop.run_until_complete(runner.run(address, port))

elif user_type == 'aggregator':
    from aggregator import aggregator_runner as runner

    loop.run_until_complete(runner.run(address, port))

elif user_type == 'leadAggregator':

    if fed_avg:
        from leadaggregator.fedavg import lead_aggregator_runner as runner
    else:
        from leadaggregator.fedshare import lead_aggregator_runner as runner

    loop.run_until_complete(runner.run(address, port))

elif user_type == 'trainer':
    client_index = int(sys.argv[5])

    if fed_avg:
        from trainer.fedavg import trainer_runner as runner
    else:
        from trainer.fedshare import trainer_runner as runner

    loop.run_until_complete(runner.run(address, port, client_index))
