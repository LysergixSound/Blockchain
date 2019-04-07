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

    def proofOfWork(self, block):
        hex_dig = hashlib.sha256(block.previous_hash).hexdigest()

        counter = 0
        while True:
            proofResult = hex_dig + str(counter)
            hash_object = hashlib.sha256(proofResult)
            proofResult = hash_object.hexdigest()

            tempResult = ""
            for x in range(0, self.difficulty):
                tempResult = tempResult + "0"

            if proofResult[:difficulty] == tempResult:
                block.proof = counter
                block.difficulty = self.difficulty
                break

            counter += 1

        return block
