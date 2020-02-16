from utils import B2Base

class B2Upload(B2Base):
    def __init__(self):
        B2Base.__init__(self)

    async def part(self):
        print("foobar")