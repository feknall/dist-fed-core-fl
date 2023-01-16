s = ""
for trainer_id in range(1, 17):
    port = trainer_id + 6000
    s += f"""trainer{trainer_id}:
        container_name: fl-trainer{trainer_id}.example.com
        image: hmaid/hyperledger:dist-fed-core-fl
        tty: true
        stdin_open: true
        labels:
          service: trainer-core
        command:
          - "trainer"
          - "localhost"
          - "{port}"
          - "0"
          - "{trainer_id - 1}"
        network_mode: "host"
    """

final_s = f"""version: "3.9"
services:
    leadAggregator:
      container_name: fl-leadAggregator.org2.example.com
      image: hmaid/hyperledger:dist-fed-core-fl
      tty: true
      stdin_open: true
      labels:
        service: leadAggregator-core
      command:
        - "leadAggregator"
        - "localhost"
        - "8082"
        - "1"
      network_mode: "host"
    {s}
"""
with open('docker-compose-fl-fedshare.yml', 'w') as f:
    f.write(final_s)
    print('Done')

