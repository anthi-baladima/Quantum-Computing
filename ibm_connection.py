from qiskit_ibm_provider import IBMProvider
from qiskit import execute
from qiskit.tools.monitor import job_monitor

def save_account():
    '''
    Saving the user's token to connect to IBM accound.
    It only needs to run if the account is not already saved.
    '''
    my_token = input("Paste IBM token:")
    IBMProvider.save_account(token=my_token)

def run(circuit, backend = "ibmq_qasm_simulator", shots = 2048):
    '''
    Run a circuit on an IBM backend.
    Used for simplicity. Default shots = 2048
    Output: job.result().get_counts()
    '''
    if not len(IBMProvider.saved_accounts()):
        save_account()
    provider = IBMProvider()
    backend = provider.get_backend(backend)
    job = execute(circuit, backend, shots=shots)
    job_monitor(job)
    counts = job.result().get_counts()
    return counts