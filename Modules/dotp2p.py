import hashlib

class API:
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def verifiyData(self, block):
        proofResult = block.previous_hash + str(block.proof)
        proofResult = hashlib.sha256(proofResult).hexdigest()

        tempResult = ""
        for x in range(0, self.difficulty):
            tempResult = tempResult + "0"

        if proofResult[:self.difficulty] == tempResult:
            return True
        else:
            return False
