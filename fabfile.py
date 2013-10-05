from fabric.api import local, settings, env, abort, run, cd, lcd
from fabric.contrib.console import confirm
from fabric.contrib.files import first, exists
from os.path import join
import os

def clean_releases():
	local("rm -rf /Users/joe/Fabric-Test/releases/")

def test():
	run('uname -s')

def release(name, directory):
	releases_directory = join(directory, 'releases')

	with lcd(directory):
		pull = local("git pull", capture=True).rstrip()

		if pull == "Already up-to-date.":
			print("Photocalls-Website is already up-to-date!")

		commit = local("git rev-parse HEAD", capture=True)
		commit = commit[:8]

		if not exists(releases_directory):
			os.makedirs(releases_directory)

		with lcd(releases_directory):
			with settings(warn_only=True):
				if not exists(join(releases_directory, 'RELEASE')):
					local("touch RELEASE")
					# local("echo '%s' > RELEASE" % commit)

				if exists(join(releases_directory, commit)):
					print("%s is already localning commit %s, aborting!" % (name, commit))
					return

				local("echo '%s' > RELEASE" % commit)
				
				last_release = local("cat RELEASE", capture=True).rstrip()

				if last_release:
					print("%s is being upraded from commit %s to commit %s." % (name, last_release, commit))
				else:
					print("%s has no releases, creating initial release." % name)

				os.makedirs(join(releases_directory, commit))
				# local("mkdir -p %s" % join(release, commit))

				with lcd(directory):
					local("git archive master | tar -x -C %s" %  join(releases_directory, commit))

				with lcd(releases_directory):
					with settings(warn_only=True):
						local("test -L current && rm -f current")

					local("ln -s %s %s" % (commit, 'current'))
					print("%s is now at commit %s" % (name, commit))

def local_deploy_test():
	release("Fabric-Test", "/Users/joe/Fabric-Test/")


def deploy_test():
	release("Fabric-Test", "/home/photocalls/fabrictest/")
