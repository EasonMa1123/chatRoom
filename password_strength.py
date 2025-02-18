class password_strength_checker:
    def __init__(self):
        self.score = 0
        self.alpha = False
        self.number = False
        self.symbol = False
        self.symbol_list = ["[","@","_","!","#","$","%","^","&","*","(",")","<",">","?","/","\",","}","{","~",":","]"]

    def password_check(self,password):
        self.score+=len(password)
        if len(password) > 25:
            self.score -= len(password)//5
        for i in str(password):
            if not self.alpha:
                if i.isalpha():
                    self.score += 5
                    self.alpha = True
            if not self.number:
                if i.isdecimal():
                    self.score += 5
                    self.number = True
            if i in self.symbol_list:
                self.score += 10
                self.symbol = True
        return self.score    
    
