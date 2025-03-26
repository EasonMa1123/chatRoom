"""
Password strength checker module.
This module provides functionality to evaluate the strength of passwords based on various criteria:
- Length
- Presence of alphabetic characters
- Presence of numbers
- Presence of special symbols
"""

class password_strength_checker:
    """
    Class that evaluates password strength based on multiple criteria.
    Assigns a score to passwords based on their characteristics.
    """
    
    def __init__(self):
        """
        Initialize the password strength checker.
        Sets up scoring variables and defines valid special symbols.
        """
        self.score = 0  # Total password strength score
        self.alpha = False  # Flag for alphabetic characters
        self.number = False  # Flag for numeric characters
        self.symbol = False  # Flag for special symbols
        # List of valid special symbols for password strength evaluation
        self.symbol_list = ["[","@","_","!","#","$","%","^","&","*","(",")","<",">","?","/","\",","}","{","~",":","]"]

    def password_check(self,password):
        """
        Evaluate the strength of a password.
        
        Scoring criteria:
        - Base score: Length of password
        - Penalty: -1 point for every 5 characters over 25
        - Bonus: +5 points for first alphabetic character
        - Bonus: +5 points for first numeric character
        - Bonus: +10 points for each special symbol
        
        Args:
            password (str): Password to evaluate
            
        Returns:
            int: Password strength score
        """
        self.score+=len(password)  # Base score from length
        if len(password) > 25:
            self.score -= len(password)//5  # Penalty for very long passwords
            
        for i in str(password):
            # Check for alphabetic characters
            if not self.alpha:
                if i.isalpha():
                    self.score += 5
                    self.alpha = True
                    
            # Check for numeric characters
            if not self.number:
                if i.isdecimal():
                    self.score += 5
                    self.number = True
                    
            # Check for special symbols
            if i in self.symbol_list:
                self.score += 10
                self.symbol = True
                
        return self.score    
    
