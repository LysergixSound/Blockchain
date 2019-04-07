class API:
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def verifiyData(self, block):
        proofResult = block.proof * block.previous_hash
        proofResult = str(proofResult)

        tempResult = ""
        for x in range(0, difficulty):
            tempResult = tempResult + "0"

        if proofResult[:difficulty] == tempResult:
            return True
        else:
            return False
