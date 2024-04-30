import sys
import xml.etree.ElementTree as et
import re



treeNew = et.parse("notes.xml")

treeNew.write("test.xml")
