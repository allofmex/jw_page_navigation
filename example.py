#!/usr/bin/python3
from src.jw_page_navigation.MailingHelper import MailingHelper
import asyncio, os
import markdown

SCRIPT_PATH = os.path.dirname(__file__)
BASE_PATH = SCRIPT_PATH

async def test():
    path = f"{BASE_PATH}/tmp/firefox-profile"
    tool = MailingHelper(path)
    # tool.setCredentials("MyPresetUsername", None)
    await tool.load()
    await tool.startNewMail()
    await tool.setSubject("Mail subject")
    await tool.setBody(createTemplate())
    await tool.setTo(["test@test.de", "test2@test.de"])
    
def createTemplate():
    f = open(BASE_PATH + "/example/template.md", "r")
    text = f.read()
    fromMarkdown = markdown.markdown(text).replace('\r', '').replace('\n', '')
    # print(fromMarkdown)
    return fromMarkdown

async def main():
    print("This is an example how to use this module")
    await test()
    print("Mail configured, you may send it now manually. We are done here.")
    
if __name__ == "__main__":
    asyncio.run(main())
