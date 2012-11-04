#! /usr/bin/env ruby
#
class Song
  @@plays = 0
  attr_reader :name, :artist, :duration
  attr_writer :duration
  def initialize (name, artist, duration)
    @name     = name
    @artist   = artist
    @duration = duration
    @plays    = 0
  end
  def to_s
    "Song: #@name---#@artist (#@duration)"
  end
  def duration_in_min
    @duration/60.0	#force floating point
  end
  def duration_in_min=(new_duration)
    @duration = (new_duration*60).to_i
  end
  def play
    @plays += 1
    @@plays += 1
    "This song: #@plays plays, Total: #@@plays plays."
  end
end

song = Song.new("don't cry", "Gun's N Rose's", 288)
puts song.to_s
song.duration_in_min = 4.2
printf("The Name of the Song: [%s], The Artist: [%s], Duration: [%d]\n", song.name, song.artist, song.duration)
song.duration = 305
printf("The Name of the Song: [%s], The Artist: [%s], Duration: [%d]\n", song.name, song.artist, song.duration)
puts song.play

class GNRSong < Song
  def initialize (name, artist, duration, lyrics)
    super(name, artist, duration)
    @lyrics = lyrics
  end
  def to_s
    super + " [#@lyrics]"
  end
  attr_reader :lyrics
end

song2 = GNRSong.new("nobody's fool", "Cinderella", "4.03", "no..no..no..no..")
puts song2.to_s
printf("Here is the Lyrics of [%s]: [%s]\n", song2.name, song2.lyrics)
puts song2.play

song3 = Song.new("rock you", "Queen", 415)
puts song3.play

class MyLogger
  private_class_method :new
  @@logger = nil
  def MyLogger.create
    @@logger = new unless @@logger
    @@logger
  end
end

puts MyLogger.create.object_id
