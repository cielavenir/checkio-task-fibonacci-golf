#!/usr/bin/env ruby

# Print "compiled size".
# Note: if MAJOR or MINOR version (libruby.so version) changes,
# rejudge is required (TEENY does not matter).

if __FILE__==$0
	if ARGV.empty?
		STDERR.puts 'local_checker rb...'
		exit
	end
	RubyVM::InstructionSequence.compile_option=true
	ARGV.each{|e|
		begin
			compile=RubyVM::InstructionSequence.new(File.read(e))
			# It seems iseq gem goes this way
			# RubyVM::InstructionSequence.load(compile.to_a)
			puts Marshal.dump(compile.to_a).size
		rescue SyntaxError => e
		end
	}
end