import re

xcel_str = '''
Catalogue entry:
See object file for catalogue entry essay by RSM.

"Comments on authenticity, quality, and glyphs":
"It is authentic. Needs to be exhibited, perhaps in a series w/other bowls. It is well painted, had a good finish. Due to burial, acid or salt eats away surface. Notice the ABACA...etc. design. Star"" (four dots). ""Bah"" means gopher. ""Lamat"" (Venus) appears also."""

Comments on glyphs:
"Same analysis here as with 1990.11.81:  scribal play; artist knows what it should be like; uses pedestal glyph (?); glyphs before/ God N glyph=her its comes;"" complex repeat: abcabcbdebcbcbcfg (head/ba)b.""  RSM coins=a pseudo sentence not a pseudo glyph.    RJ: d=2 round dots over pop (mat); g=animal; also lamat (Venus)"""

Comment on text and future interpretation:
"Both (1990.011.91 also) come from the same area; Lowland. If can draw out text, Dorie will look at further and try to translate; could invite student/young epigraphers in to read and interpret. Or--send photographs?"

Use for fixed compensation paid regularly to employees for ongoing work or services, on the basis of periods longer than days. For such compensation paid on an hourly, daily, or piecework basis, use "wages."

May 1993 related term added. February 1993 descriptor moved.

location verified, inventory 2001.  Turner inventory, April 2004.  Location verified, inventory 9, Winter 2005.

Purchase date and method taken from lists attached to donor tax forms (see accession lot).  Source taken from handwritten receipt found in donor files (see accession lot).
'''

str = '''
Hello
"This is a ""good"" example of ""work"""
Testing
"Hello"
'''

new_str = str.replace('""', "'")

pattern = r'"(.*?)"'

matches = re.findall(pattern, new_str)

print(matches)