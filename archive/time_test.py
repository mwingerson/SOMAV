
import time

my_time = time.time()

print "my_time: %d", my_time

print "time: %d", time.time()

while ((time.time() - my_time) < 2):
		print "shitty"

print "I'm awesome"