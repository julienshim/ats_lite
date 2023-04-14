# ██████╗  █████╗ ██████╗ ████████╗     ██████╗ ███████╗    ███████╗██████╗ ███████╗███████╗ ██████╗██╗  ██╗
# ██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝    ██╔═══██╗██╔════╝    ██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝██║  ██║
# ██████╔╝███████║██████╔╝   ██║       ██║   ██║█████╗      ███████╗██████╔╝█████╗  █████╗  ██║     ███████║
# ██╔═══╝ ██╔══██║██╔══██╗   ██║       ██║   ██║██╔══╝      ╚════██║██╔═══╝ ██╔══╝  ██╔══╝  ██║     ██╔══██║
# ██║     ██║  ██║██║  ██║   ██║       ╚██████╔╝██║         ███████║██║     ███████╗███████╗╚██████╗██║  ██║
# ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝        ╚═════╝ ╚═╝         ╚══════╝╚═╝     ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝
                                                                                                                  

# CC Coordinating conjunction
# CD Cardinal number
# DT Determiner
# EX Existential there
# FW Foreign word
# IN Preposition or subordinating conjunction
# JJ Adjective
# JJR Adjective, comparative
# JJS Adjective, superlative
# LS List item marker
# MD Modal
# NN Noun, singular or mass
# NNS Noun, plural
# NNP Proper noun, singular
# NNPS Proper noun, plural
# PDT Predeterminer
# POS Possessive ending
# PRP Personal pronoun
# PRP$ Possessive pronoun
# RB Adverb
# RBR Adverb, comparative
# RBS Adverb, superlative
# RP Particle
# SYM Symbol
# TO to
# UH Interjection
# VB Verb, base form
# VBD Verb, past tense
# VBG Verb, gerund or present participle
# VBN Verb, past participle
# VBP Verb, non­3rd person singular present
# VBZ Verb, 3rd person singular present
# WDT Wh­determiner
# WP Wh­pronoun
# WP$ Possessive wh­pronoun
# WRB Wh­adverb

target_part_of_speech = ["NN", "NNS", "NNP", "NNPS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "JJ", "JJR", "JJS"]
user_defined_stop_words = ["'", ')', '#', ';', '—', '(', '’', '!', '/', '+', ',', 'a', '”', ':', '%', '–', '*', '&', '•', '?', '-', '“', '.'] # class and background are html keywords
fdist_count = 20
ngram_number = 2
ngram_min_count = 2
resume_txt_path = './assets/resume.txt'