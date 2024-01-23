

ffmpeg -i large.mp4 -r 12 -f image2 large/large-%04d.jpg
ffmpeg -i small.mp4 -r 12 -f image2 small/small-%04d.jpg


