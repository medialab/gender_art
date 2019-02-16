#OpenRefine script runned to add Institution and Town columns in the deposit network file
import re
regex1 = re.compile(r'.*?\/.*?\/.*?\s-\s(.+?)(?:\s\(en cours\))?\sDossier', flags=re.S)
regex2 = re.compile(r'(.+?)\s([^\s]+?(?:\s\(.+?\))?)$')
return regex2.match(regex1.match(value).group(1)).group(1)