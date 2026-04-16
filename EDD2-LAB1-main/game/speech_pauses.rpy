###############################################################################################################
### AUTOMATIC SPEECH PAUSES ###################################################################################
###############################################################################################################
#
# Thanks for downloading my Automatic Speech Pauses plugin for Ren'Py! ( https://kigyo.itch.io/speech-pauses-for-renpy )
#
# Now, all you need to do is adjust the pause lengths below to your liking and (optionally) add new settings to
# your preferences screen to leave the choice up to the player!
#
# If you like this tool, consider dropping a donation: https://ko-fi.com/kigyodev
# Credit to "KigyoDev" would also be appreciated!
#
# Thank you, and may this tool make your text feel more natural and alive! :D
# - KigyoDev
#
###############################################################################################################

## Variables ##################################################################################################

# Determines whether the pauses are active at all
# default value: True
default persistent.speech_pauses = True

# Determines the pause length of commas and ellipses
# default value: 0.15
default persistent.speech_pause_comma = 0.15

# Determines the pause length of periods, questions, em dashes, and so on
# default value: 0.3
default persistent.speech_pause_period = 0.3

# Determines which version of pause to use
# Version A: Generally better and suitable for the vast majority of projects, since its pause lengths are 
#            relative to the text speed, it doesn't interfere with text shaders, and it allows lines with 
#            lots of pauses to still be displayed with one click.
# Version B: Doesn't have any of the above benefits, but it adds an audible pause in case you are using 
#            text bleeps. With version 1, text bleeps keep going at a constant pace despite the visual pause, 
#            so version 2 might be more natural in that case.
# default value: "A"
define speech_pause_version = "A"

## Definitions ################################################################################################

# Define what counts as a "comma" (shorter pause)
# default value: [",", "..."]
define speech_comma = [",", "..."]

# Define what counts as a "period" (longer pause)
# default value: [".", "?", "!", ":", ";", "—", "~"]
define speech_period = [".", "?", "!", ":", ";", "—", "~"]

# Define exceptions where any of the above symbols should not lead to a pause
# default value: ["Mr.", "Mrs.", "Dr."]
define speech_exceptions = ["Mr.", "Mrs.", "Dr."]

# Define additional text tags that should not interfere with pauses. The default ones are already included
#   For example, this will make sure that a line like "{b}What?!{/b} Are you serious?" still correctly registers
#   a pause, even though "?!" is followed up by "{/b}" instead of a blank space.
# example values: ["b", "a", "i"]
# default value: []
define speech_tags = []

## Spaceless definitions ######################################################################################

# Some punctuation marks do not require a space afterwards (which is how the need for a pause is usually detected).
# I tried a hacky solution that will add a pause whenever any of the below punctuation marks appear, 
#   UNLESS they are the last character in a line.

# Feel free to disable them if this leads to unexpected behavior.
# default value: True
define speech_pauses_nospace = True

# Comma-equivalents that require no space after
# default value: ["，","、", "…", "——"]
define speech_comma_nospace = ["，","、", "…", "——"]

# Period-equivalents that require no space after
# Note: If you use em-dashes [like—this] instead of [like — this], delete them from [speech_period] and add them down here!
# default value: ["。", "？", "！", "；", "：", "……"]
define speech_period_nospace = ["。", "？", "！", "；", "：", "……"]

## The Function ###############################################################################################

init python:
    def speech_pause_adder(text_input):

        tags = speech_tags + ["i", "b", "a", "color", "s", "size", "u", "alpha", "alt", "cps", "art", "font", "image", "k", "noalt", "outlinecolor", "plain", "rb", "rt", "shader"]
        open_tags = ["space", "vspace", "w", "p", "nw", "fast", "done", "clear"]

        pauses_add = {}

        if "b" in speech_pause_version or "B" in speech_pause_version:
            for i in speech_comma:
                pauses_add[i + " "] = i + "{w=" + str(persistent.speech_pause_comma) + "} "
                for j in tags:
                    pauses_add[i + "{/" + j + "} "] = i + "{/" + j + "}{w=" + str(persistent.speech_pause_comma) + "} "
                for j in open_tags:
                    pauses_add[i + "{" + j + "} "] = i + "{" + j + "}{w=" + str(persistent.speech_pause_comma) + "} "
            for i in speech_period:
                pauses_add[i + " "] = i + "{w=" + str(persistent.speech_pause_period) + "} "
                for j in tags:
                    pauses_add[i + "{/" + j + "} "] = i + "{/" + j + "}{w=" + str(persistent.speech_pause_period) + "} "
                for j in open_tags:
                    pauses_add[i + "{" + j + "} "] = i + "{" + j + "}{w=" + str(persistent.speech_pause_period) + "} "
            
            pauses_exceptions = {}
            for i in speech_exceptions:
                pauses_exceptions[i + "{w=" + str(persistent.speech_pause_comma) + "} "] = i + " "
                pauses_exceptions[i + "{w=" + str(persistent.speech_pause_period) + "} "] = i + " "
                
            for i in pauses_add:
                text_input = text_input.replace(i, pauses_add[i])

            for i in pauses_exceptions:
                text_input = text_input.replace(i, pauses_exceptions[i])

            if speech_pauses_nospace:
                text_copy = ""
                for i in range(len(text_input)):
                    text_copy += text_input[i]
                    if i < len(text_input)-1 and text_input[i:i+2] in speech_comma_nospace or text_input[i:i+2] in speech_period_nospace:
                        continue
                    elif i > 0 and text_input[i-1:i+1] in speech_comma_nospace:
                        text_copy += "{w=" + str(persistent.speech_pause_comma) + "}"
                    elif i > 0 and text_input[i-1:i+1] in speech_period_nospace:
                        text_copy += "{w=" + str(persistent.speech_pause_period) + "}"
                    elif text_input[i] in speech_comma_nospace and i < len(text_input)-1:
                        text_copy += "{w=" + str(persistent.speech_pause_comma) + "}"
                    elif text_input[i] in speech_period_nospace and i < len(text_input)-1:
                        text_copy += "{w=" + str(persistent.speech_pause_period) + "}"
                
                text_input = text_copy

        else:
            comma_slow = (1/persistent.speech_pause_comma)/100
            period_slow = (1/persistent.speech_pause_period)/100

            for i in speech_comma:
                pauses_add[i + " "] = i + "{cps=*" + str(comma_slow) + "} {/cps}"
                for j in tags:
                    pauses_add[i + "{/" + j + "} "] = i + "{/" + j + "}{cps=*" + str(comma_slow) + "} {/cps}"
                for j in open_tags:
                    pauses_add[i + "{" + j + "} "] = i + "{" + j + "}{cps=*" + str(comma_slow) + "} {/cps}"
            for i in speech_period:
                pauses_add[i + " "] = i + "{cps=*" + str(period_slow) + "} {/cps}"
                for j in tags:
                    pauses_add[i + "{/" + j + "} "] = i + "{/" + j + "}{cps=*" + str(period_slow) + "} {/cps}"
                for j in open_tags:
                    pauses_add[i + "{" + j + "} "] = i + "{" + j + "}{cps=*" + str(period_slow) + "} {/cps}"
            
            pauses_exceptions = {}
            for i in speech_exceptions:
                pauses_exceptions[i + "{cps=*" + str(comma_slow) + "} {/cps}"] = i + " "
                pauses_exceptions[i + "{cps=*" + str(period_slow) + "} {/cps}"] = i + " "
                
            for i in pauses_add:
                text_input = text_input.replace(i, pauses_add[i])

            for i in pauses_exceptions:
                text_input = text_input.replace(i, pauses_exceptions[i])

            if speech_pauses_nospace:
                text_copy = ""
                for i in range(len(text_input)):
                    text_copy += text_input[i]
                    if i < len(text_input)-1 and text_input[i:i+2] in speech_comma_nospace or text_input[i:i+2] in speech_period_nospace:
                        continue
                    elif i > 0 and text_input[i-1:i+1] in speech_comma_nospace:
                        text_copy += "{cps=*" + str(comma_slow) + "}"
                    elif i > 0 and text_input[i-1:i+1] in speech_period_nospace:
                        text_copy += "{cps=*" + str(period_slow) + "}"
                    elif text_input[i] in speech_comma_nospace and i < len(text_input)-1:
                        text_copy += "{cps=*" + str(comma_slow) + "}"
                    elif text_input[i] in speech_period_nospace and i < len(text_input)-1:
                        text_copy += "{cps=*" + str(period_slow) + "}"
                    if (text_input[i] in speech_comma_nospace or text_input[i] in speech_period_nospace) and i < len(text_input)-1 or i > 0 and text_input[i-1:i+1] in speech_comma_nospace or i > 0 and text_input[i-1:i+1] in speech_period_nospace:
                        text_copy += "\u200B{/cps}"
            
                text_input = text_copy

        return text_input
    

    def add_speech_pauses(text_input):
        if prev_filter:
            text_input = prev_filter(text_input)

        if persistent.speech_pauses is not True or preferences.text_cps == 0:
            return text_input

        return speech_pause_adder(text_input)

    ## Initialization #############################################################################################
    # If your project already makes use of [config.say_menu_text_filter], this makes sure
    # your filter is also called in addition to this one.

    prev_filter = config.say_menu_text_filter
    config.say_menu_text_filter = add_speech_pauses

## Licence ####################################################################################################

# Copyright 2025 KigyoDev

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions 
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
