s = ""
for trainer_id in range(1, 17):
    port = trainer_id + 6000
    s += f"""trainer{trainer_id}:
        container_name: trainer{trainer_id}.example.com
        image: hmaid/hyperledger:dist-fed-gateway
        labels:
          service:
        volumes:
          - ${{DIST_FED_CREDENTIAL_HOME}}:/credential
        command:
          - "--fl.chaincode.name=fedavg-chaincode"
          - "--fl.role=trainer"
          - "--trainer.org1.cert.path=/credential/peerOrganizations/org1.example.com/users/Trainer{trainer_id}@org1.example.com/msp/signcerts/cert.pem"
          - "--trainer.org1.key-dir.path=/credential/peerOrganizations/org1.example.com/users/Trainer{trainer_id}@org1.example.com/msp/keystore"
          - "--trainer.org1.tls-cert.path=/credential/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt"
          - "--trainer.org1.organization=org1.example.com"
          - "--trainer.org2.cert.path=/credential/peerOrganizations/org2.example.com/users/Trainer{trainer_id}@org2.example.com/msp/signcerts/cert.pem"
          - "--trainer.org2.key-dir.path=/credential/peerOrganizations/org2.example.com/users/Trainer{trainer_id}@org2.example.com/msp/keystore"
          - "--trainer.org2.tls-cert.path=/credential/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt"
          - "--trainer.org2.organization=org2.example.com"
          - "--server.port={port}"
        ports:
          - "{port}:{port}"
        network_mode: "host"
    """

final_s = f"""version: "3.9"
services:
    {s}
"""
with open('docker-compose-gateway-trainer.yml', 'w') as f:
    f.write(final_s)