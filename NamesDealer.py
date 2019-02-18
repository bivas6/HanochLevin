def no_nikkud(w): ## strip names from the NIKKUD and make one word. המלך דוד >> המלך_דוד
        lw = w.replace(' ', '_')
        w_ = ''
        for c in lw:
            if (c<='ת' and c>='א') or c == '-' or c == '_':
                w_ += c
        return w_


    
class NamesDealer:
    def __init__(self):
        self.NP = ['איש','בהמון','שליח' ,'אחד','לוקה','סריס','של','זונה','עם','כרוב','שיכור','','זקיף', 'צופה', 'קבצן', 'מבשר', 'עוני', 'מלאך','מחשבת','מחשבה','החייל','השכן','ילד', 'חייל','אשה', 'נוסע','רוצח', 'גדול', 'עולם', 'משרת', 'מת', 'מתה','אם', 'שוליית', 'בכיין', 'ילד', 'רופא', 'גוסס', 'רופא']
        self.NPish = ['איש','שליח','סריס','זקיף', 'צופה', 'רוצח','קבצן', 'מלאך','החייל', 'חייל','אשה', 'משרת', 'מת', 'מתה','אם', 'ילד', 'רופא','שיכור','כרוב','זונה']
    
    @staticmethod
    def store_format(self, w):
        return no_nikkud(w)

    def print_format(self, w):
        return self.rev(w)

    def more_then_one(self, w): ## identify when it's more then one speaker. פופר ושלמה
        lw = w.split('_')
        try:
            lw.remove('')
        except:
            pass
        return len(lw) == 2 and not lw[1] in self.NP and lw[1][0] == 'ו'


    def rev(self, w): ## for some reason the labels need to be reversed
        if not isinstance(w ,str):
            return w
        w_=''
        for c in w:
            w_ = c + w_
        return w_.replace('_', ' ')

    def all_NP(self, nl):
        for w in nl:
            if w not in self.NP:
                return False
        return True

    def can_unify_all_NP(self, n1l, n2l):
        for w in n1l:
            if w not in self.NPish: 
                continue
            for w2 in n2l:
                if w2 not in self.NPish:
                    continue
                if self.can_unify_one(w, w2):
                    return True
        return False


    def can_unify(self, n1, n2): ## check for specific 2 names if they referenced to the same chracter
        n1l, n2l = (n1.split('_'), n2.split('_')) if len(n1) > len(n2) else (n2.split('_'), n1.split('_'))
        if self.all_NP(n1l):
            return self.can_unify_all_NP(n1l, n2l)
        if self.all_NP(n2l):
            return self.can_unify_all_NP(n2l, n1l)
        for w1 in n1l:
            if w1 == '' or w1 in self.NP: continue
            for w2 in n2l:
                if w2 in self.NP: continue
                if self.can_unify_one(w1, w2):
                    return True
        return False

    def can_unify_one(self, w1, w2): ## check if w1 and w2 can be unify
        if abs(len(w1) - len(w2)) > 1 :
            return False
        return self.at_most_one(w1, w2)   # same word
         

    def at_most_one(self, w1, w2): ## names that different in at most 1 char are the same: נסיכה == נסיכת, ופופר == פופר
        t = 0
        if len(w1) > len(w2):
            l1, i, l2 = (w1, 1, w2)
        elif len(w2) > len(w1):
            l1, i, l2 = (w2, 1, w1)
        else:
            l1, i, l2 = (w2, 0, w1)
        for j in range(len(l2)):
            if l1[j +i] == l2[j]:
                t += 1
        return len(l2) -t <=1        

    def unify(self, characters): ## in case that same charcter use different names, unify them to the detailed one.  הנסיכה >> הנסיכה של מונקו 
        #Tracer()()
        un_characters = characters[:]
        for i in range(len(characters)):         
            for j in range(i+1, len(characters)):
                if self.can_unify(characters[i], characters[j]):
                    rem = self.better_choice_to_rem(characters, i, j)
                    try:
                        un_characters.remove(rem)
                    except:
                        pass
        return un_characters
    
    def better_choice_to_rem(self,characters, i, j): ## in case that 2 names are the same, choose who to delete
        if self.more_then_one(characters[i]):
            return characters[i]
        if self.more_then_one(characters[j]):
            return characters[j]
        return characters[i] if len(characters[i].split('_')) < len(characters[j].split('_')) else characters[j]
  