import re

from constants.constants import Constants


class string_utils:
    @staticmethod
    def find_sub_word(term, ent_list):
        found_list = []
        for word in ent_list:
            ptrn = string_utils.replaceSpecialChars(word)
            if re.search("(\\b\\s*|^)" + ptrn + "(\\s*\\b|$)", term.lower()) and word.lower() != term.lower():
                found_list.append(word)
        return found_list

    @staticmethod
    def clean_sub_strings_from_list(ent_list):
        copy_list = [x.lower() for x in ent_list]
        copy_list = list(set(copy_list))

        # copy_list=sorted(copy_list,key=len,reverse=False)
        for ent in sorted(copy_list,key=len,reverse=True):
           found_list= string_utils.find_sub_word(ent,sorted(copy_list,key=len,reverse=False))
           for found in found_list:
               if found != None:
                   copy_list.remove(found)
        return copy_list

    @staticmethod
    def replacenonescapechars(sent):
        sent_rep = re.sub("[~\-^{}\\[\\]\\\\:;\\(\\)\"<>?*|!=]\.", " ", sent)
        sent_rep = re.sub("\\s+", " ", sent_rep)
        sent_rep = re.sub("\\\$", " ", sent_rep)
        return sent_rep.strip()

    @staticmethod
    def replaceEscapeChars(word):
        escaped = re.sub("\+", r"\+", word)
        escaped = re.sub("\.", r"\.", escaped)
        escaped = re.sub("#", r"\#", escaped)
        escaped = re.sub("&", r"\&", escaped)
        return escaped

    @staticmethod
    def replaceSpecialChars(word):
        word_reg = string_utils.replacenonescapechars(word)
        word_reg = string_utils.replaceEscapeChars(word_reg)
        return word_reg


    @staticmethod
    def get_all_entities_as_map(entities):
        ent_map = {}
        ent_map[Constants.category]=[]
        ent_map[Constants.pos_entities]=[]
        ent_map[Constants.location] = []
        ent_map[Constants.skills] = []
        ent_map[Constants.skills_] = []
        ent_map[Constants.cities] = []
        ent_map[Constants.states] = []
        ent_map[Constants.countries] = []
        ent_map[Constants.cities_] = []
        ent_map[Constants.states_] = []
        ent_map[Constants.countries_] = []
        ent_map[Constants.user_fullname] = []
        for ent in entities:
            if ent[Constants.entity] in Constants.SLOTS_DEFAULT:
                ent_map[ent[Constants.entity]].append(ent[Constants.value])
                # ent_map[ent[Constants.entity]].append(ent[Constants.value].lower())
            else:
                ent_map[ent[Constants.entity]] = []
        return ent_map

    @staticmethod
    def normalize(s):
        """
        Given a text, cleans and normalizes it. Feel free to add your own stuff.
        """
        s = s.lower()
        # Replace ips
        s = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ' _ip_ ', s)
        # Isolate punctuation
        s = re.sub(r'([\'\"\.\(\)\!\?\-\\\/\,])', r' \1 ', s)
        # Remove some special characters
        s = re.sub(r'([\;\:\|•«\n])', ' ', s)
        # Replace numbers and symbols with language
        s = s.replace('&', ' and ')
        s = s.replace('@', ' at ')
        s = s.replace('0', ' zero ')
        s = s.replace('1', ' one ')
        s = s.replace('2', ' two ')
        s = s.replace('3', ' three ')
        s = s.replace('4', ' four ')
        s = s.replace('5', ' five ')
        s = s.replace('6', ' six ')
        s = s.replace('7', ' seven ')
        s = s.replace('8', ' eight ')
        s = s.replace('9', ' nine ')
        return s



if __name__ == '__main__':
    s=string_utils.normalize('Who is your ceo?')
    print(s)