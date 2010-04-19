#!/usr/bin/env python
import twitter
import re
from optparse import OptionParser
from sys import exit, exc_info
from urllib2 import URLError

class Main:
    colors = {
        "grey":"\033[1;30m",
        "red":"\033[1;31m",
        "green":"\033[1;32m",
        "blue":"\033[1;34m",
    }

    KILL = "\033[1;m"

    def Color(self, str, color):
        return self.colors[color] + str + self.KILL

    def __init__(self, user = None, passw = None):
        self.twitter = twitter.Api(username = user, password = passw)

    def TimeLine(self, user = None):
        try:
            timeLine = self.twitter.GetFriendsTimeline(user)
        except URLError as e:
            print(e)
            exit(1)
        except:
            raise

        timeLine.reverse()
        for status in timeLine:
            user = self.Color(status.user.name, "blue")
            date = self.Color(status.relative_created_at, "grey")
            text = re.sub("@(\w+)", lambda x: self.Color(x.group(0), "green"), status.text)
            text = re.sub("#(\w+)", lambda x: self.Color(x.group(0), "red"), text)

            print "%s - %s:\n%s\n" % (user, date, text)

    def PostStatus(self, status):
        if len(status) > 0 and len(status) <= 140:
            self.twitter.PostUpdate(status)
            self.TimeLine()
        else:
            print("Status length too long or too short: ", len(status))

if __name__ == "__main__":
    opt = OptionParser()
    opt.add_option("-u", "--user", dest = "user", help = "Twitter login name")
    opt.add_option("-p", "--password", dest = "passw", help = "Twitter login password", metavar = "PASSWORD")
    opt.add_option("-s", "--status", dest = "status", help = "Post a status update")
    #opt.add_option("-l", "--limit", dest = "limit", help = "Feed length limit", type = "int", default = 10)

    (opts, args) = opt.parse_args()

    if not opts.user or not opts.passw:
        if opts.user:
            from getpass import getpass
            opts.passw = getpass()
        else:
            print("User name not specified")
            exit(1)

    inst = Main(user = opts.user, passw = opts.passw)

    if opts.status:
        inst.PostStatus(opts.status)
    else:
        inst.TimeLine()
