class Enum {
    def initval = 0;
    def count = 0;
    func __init__(self, initval) {
        self.count = self.initval = initval;
        return null;
    }
    func reset(self) {
        self.count = self.initval;
        return null;
    }
    func enum(self) {
        def temp = self.count;
        self.count += 1;
        return temp;
    }
}