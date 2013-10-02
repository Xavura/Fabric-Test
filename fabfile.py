from fabric.api import local, settings, env, abort, run, cd, lcd
from fabric.contrib.console import confirm
from fabric.contrib.files import first
from os.path import join, exists
import os

def release(name, directory):
	releases_directory = join(directory, 'releases')

	with lcd(directory):
		pull = local("git pull", capture=True).rstrip()

		if pull == "Already up-to-date.":
			print("Photocalls-Website is already up-to-date!")
			return

			commit = local("git rev-parse HEAD", capture=True)
			commit = commit[:8]

		with lcd(releases_directory):
			with settings(warn_only=True):
				if not exists(join(releases_directory, 'RELEASE')):
					print("Photocalls-Website has no releases, creating initial release.")

					local("touch RELEASE")
					local("echo '%s' > RELEASE" % commit)
				else:
					last_release = local("cat RELEASE", capture=True).rstrip()

					if exists(join(releases_directory, commit)):
						print("%s is already running commit %s, aborting!" % (name, commit))
						return

					local("echo '%s' > RELEASE" % commit)

					print("Photocalls-Website is being upraded from commit %s to commit %s." % (last_release, commit))

					local("mkdir -p %s" % join(release, commit))

					with lcd(commit):
						local("git archive master | tar -x -C %s" %  join(releases_directory, commit))

					with lcd(releases_directory):
						with settings(warn_only=True):
							local("test -f current && rm -f current")

						local("ln -s %s %s" % (commit, 'current'))
						print("%s is now at commit %s" % (name, commit))

def local_deploy_test():
	release("Fabric-Test", "/Users/joe/Fabric-Test/")
