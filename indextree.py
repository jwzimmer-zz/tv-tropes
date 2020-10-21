#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:22:25 2020

@author: jzimmer1, philnguyen
"""

from bs4 import BeautifulSoup
import re
import pickle
import os
import pandas as pd

#this is the dictionary this script outputs for "Indices/Genre Tropes - TV Tropes.htm":
# =============================================================================
# 
# {' Sub-indexes:': ['Action/Adventure Tropes', 'Advertising Tropes', 'Alternate History Tropes', 'Comedy Tropes', 'Recorded and Stand-Up Comedy', 'Crime and Punishment Tropes', 'Drama Tropes', 'Espionage Tropes', 'Fairy Tale Tropes', 'Game Show Tropes', 'Genre Title Grab Bag', 'Horror Tropes', 'Love Tropes', 'Military and Warfare Tropes', 'Mystery Tropes', 'News Broadcast', 'News Tropes', 'Ninja Tropes', 'Opera', 'Picaresque', 'Pirate Tropes', 'Post-9/11 Terrorism Movie', 'Professional Wrestling', 'Reality TV Tropes', 'Romance Novel Tropes', 'Speculative Fiction Tropes', 'Sports Story Tropes', 'Superhero Tropes', 'Thriller', 'Tragedy', 'Tokusatsu Tropes', 'Wild West Tropes'], ' Tropes related directly to Genres:': ['Contractual Genre Blindness', 'Death by Genre Savviness', 'From Clones to Genre', 'Functional Genre Savvy', 'Gameplay Roulette', 'Genre Adultery', 'Genre Blindness', 'Genre-Busting', 'Genre Deconstruction', 'Genre-Killer', 'Genre Mashup', 'Genre Motif', 'Genre Refugee', 'Genre Relaunch', 'Genre Roulette', 'Genre Savvy', 'Genre Shift', 'Genre Throwback', 'Genre Turning Point', 'Heavy Meta', 'Out-of-Genre Experience', 'Reality Show Genre Blindness', 'Sliding Scale of Comedy and Horror', 'Unexpected Gameplay Change', 'The Universal Genre Savvy Guide', 'Wrong Genre Savvy']}
# 
# =============================================================================

#Here's the output if I run this script on the Indices folder and ignore encoding issues
# =============================================================================
# 
# {}
# {}
# {'Index of subwikis with icons:': ['Administrivia', 'Analysis', 'Awesome', 'Awesome Music', 'Characters', 'Darth Wiki', 'Discontinuity', 'Fan Works', 'Fanfic Recs', 'Fridge', 'Funny', 'Headscratchers', 'Ho Yay', 'Heartwarming', 'Horrible', 'Laconic', 'Nightmare Fuel', 'Pantheon', 'Quotes', 'Radar', 'Recap', 'Self Demonstrating', 'Shout-Out', 'So You Want To', 'Sugar Wiki', 'Tear Jerker', 'WMG', 'YMMV'], 'Index of subwikis without icons:': ['And the Fandom Rejoiced', 'Complete Monster', 'Haiku', 'Image Links', 'Memes', 'Playing With', 'Referenced by...', 'Timeline', 'Useful Notes']}
# {'Tropes:': ['Averted Trope', 'Bait-and-Switch', 'Characteristic Trope', 'Conversational Troping', 'Cyclic Trope', 'Dead Horse Trope', 'Dead Unicorn Trope', 'Dead Horse Trope', 'Deconstructed Trope', 'Defied Trope', 'Discredited Trope', 'Discussed Trope', 'Double Subversion', 'Downplayed Trope', 'Enforced Trope', 'Moral Guardians', "Everything's Worse with Snowclones", 'Evolving Trope', 'Exaggerated Trope', 'Exploited Trope', 'Forgotten Trope', 'Gender-Inverted Trope', 'Implied Trope', 'Intended Audience Reaction', 'Audience Reaction', 'Inverted Trope', 'Invoked Trope', 'Justified Trope', 'Lampshade Hanging', 'Logical Extreme', 'Necessary Weasel', 'Newer Than They Think', 'Not a Deconstruction', 'Not a Subversion', 'Older Than They Think', 'Omnipresent Tropes', 'Overdosed Tropes', 'Parodied Trope', 'Pet-Peeve Trope', 'Played for Drama', 'Played for Horror', 'Nightmare Fuel', 'Played for Laughs', 'Playing with a Trope', 'Sister Trope', 'Spoilered Rotten', 'Square Peg, Round Trope', 'Trope Decay', 'Sub-Trope', 'Subverted Trope', 'Super-Trope', 'Trope', 'Trope Breaker', 'Trope Decay', 'Trope Enjoyment Loophole', 'Pet-Peeve Trope', 'Trope Grid', 'Troperiffic', "Troper's Block", 'Trope Namer Syndrome', 'YKTTW', 'Tropes Are Flexible', 'Tropes Are Tools', 'Tropes in Aggregate', 'Trope Telegraphing', 'Undead Horse Trope', 'Dead Horse Trope', 'Unbuilt Trope', 'Zig-Zagging Trope']}
# {'Tropes': ['The Antagonist', 'Villain Antagonist', 'Anthropic Principle', 'Black Dot Pupils', 'Characters', 'The Climax', 'Conflict', 'Consistency', 'Contrived Coincidence', 'Dénouement', 'Fantasy Gun Control', 'Fire Is Red', 'Fourth Wall', 'The Good Guys Always Win', 'Happy Ending', 'Hit Spark', 'Inciting Incident', 'Infinite Stock For Sale', 'Narrative Beats', 'Official Couple', 'Plot', 'Plot Device', 'Plot Point', 'Point of View', 'The Protagonist', 'Hero Protagonist', 'Punchline', 'Recurring Character', 'Rising Conflict', 'Rounded Character', 'Settings', 'Third-Person Flashback', 'Three-Month-Old Newborn', 'Time Marches On', 'Water Is Blue']}
# {}
# {'Examples of the following go in the Trivia tab:': ['Ability over Appearance', 'Accent Depundent', 'Accidentally Correct Writing', 'Accidentally Correct Zoology', 'Acclaimed Flop', 'Acting for Two', 'Acting in the Dark', 'Actor Existence Limbo', 'Actor-Inspired Element', 'improvised', 'Actor-Shared Background', 'Adaptation First', 'Adaptation Overdosed', 'Adaptation Sequence', 'Adored by the Network', 'Alan Smithee', 'All-Star Cast', 'Amateur Cast', 'Anime First', 'Anonymous Author', 'Approval of God', 'Artist Disillusionment', 'Ascended Fanon', 'Ashcan Copy', 'Attention Deficit Creator Disorder', 'Author Existence Failure', 'Development Hell', 'Author Phobia', 'Award Category Fraud', 'Awesome, Dear Boy', 'Baby Name Trend Starter', 'Backed by the Pentagon', 'Bad Export for You', 'Banned Episode', 'Banned In China', 'Based on a Dream', 'Beam Me Up, Scotty!', 'Big Name Fan', 'Billing Displacement', 'Black Sheep Hit', 'Blooper', 'Bonus Episode', 'Bonus Material', 'Box Office Bomb', 'Breakaway Advertisement', 'Breakaway Pop Hit', 'Breakup Breakout', 'Breakthrough Hit', 'B-Team Sequel', '...But I Play One on TV', 'California Doubling', 'Cameo Prop', 'Cancellation', 'Career Resurrection', 'obscurity', 'stages a successful comeback', 'Cash Cow Franchise', 'Cast the Expert', 'Cast the Runner-Up', 'Cast Incest', 'The Cast Showoff', 'Celebrity Break-Up Song', 'Break Up Song', 'Celebrity Voice Actor', 'Channel Hop', 'The Character Died with Him', 'The Character Ice Cream Bar', 'Uncanny Valley', 'Character Outlives Actor', 'Chart Displacement', 'Children Voicing Children', 'Christmas Rushed', 'Colbert Bump', 'Completely Different Title', 'Content Leak', 'Contest Winner Cameo', 'Contractual Immortality', 'Contractual Obligation Project', 'Contractual Purity', 'Moral Guardians', 'Copiously Credited Creator', 'Cowboy BeBop at His Computer', 'Creative Differences', 'Creator Backlash', 'Creator Breakdown', 'Creator Couple', 'Music', 'Creator Killer', 'Creator-Preferred Adaptation', 'Creator Recovery', "Creator's Apathy", "Creator's Favorite", "Creator's Favorite Episode", "Creator's Oddball", "Creator's Pest", 'Cross-Dressing Voices', 'Cross-Regional Voice Acting', 'The CSI Effect', 'Real Life', 'Cut Song', 'The Danza', 'Darkhorse Casting', 'Dawson Casting', 'Dear Negative Reader', 'Defictionalization', 'Delayed Release Tie-In', 'Deleted Role', 'Deleted Scene', 'Deliberate Flaw Retcon', 'Demand Overload', 'Denied Parody', 'Descended Creator', 'Development Gag', 'Development Hell', 'Directed by Cast Member', 'Direct-to-Video', 'Disabled Character, Disabled Actor', 'Disowned Adaptation', 'Distanced from Current Events', 'Real Life', 'Divorced Installment', 'Doing It for the Art', 'Doubling for London', 'Drawing Board Hiatus', 'retooled', 'Dueling Dubs', 'Dueling Products', 'Dueling-Stars Movie', 'Dueling Works', 'DVD Commentary', 'Dye Hard', 'Dyeing for Your Art', 'Early-Bird Release', 'Early Draft Tie-In', 'Edited for Syndication', 'Enforced Method Acting', '#EngineeredHashtag', 'viral', 'Executive Meddling', 'Executive Veto', 'Exiled from Continuity', 'Extremely Lengthy Creation', 'Fake Nationality', 'Fake American', 'Fake Australian', 'Fake Brit', 'Fake Scot', 'Fake Irish', 'Fake Mixed Race', 'Fake Russian', 'Fan Community Nicknames', 'Fan Nickname', 'Fandom Life Cycle', 'Fandom Nod', 'Fan Translation', 'Fanwork Ban', 'Fatal Method Acting', 'Filming Location Cameo', 'California Doubling', 'First Appearance', 'Five Year Plan', 'Flagship Franchise', 'Flip-Flop of God', 'Focus Group Ending', 'Foiler Footage', 'Cliffhanger', 'Follow the Leader', 'Follow-Up Failure', 'Font Anachronism', 'Fountain of Expies', 'Franchise Killer', 'Film', 'Video Games', 'Franchise Zombie', 'Friday Night Death Slot', 'From Entertainment to Education', 'Full Circle Portraying', 'Funny Character, Boring Actor', 'Gay Panic', 'Moral Guardians', 'Genre Adultery', 'Genre-Killer', 'Genre Popularizer', 'God Created Canon Foreigner', 'God Does Not Own This World', 'God Never Said That', 'Half-Remembered Homage', 'Harpo Does Something Funny', 'He Also Did', "Hey, It's That Gun!", "Hey, It's That Place!", "Hey, It's That Sound!", 'Hide Your Pregnancy', 'Hire the Critic', 'Hitless Hit Album', 'Hostility on the Set', 'Humble Beginnings', 'Cash Cow Franchise', 'I Am Not Spock', 'I Knew It!', 'Image Source', 'Incestuous Casting', 'In Memoriam', 'Inspiration for the Work', 'International Coproduction', 'Invisible Advertising', 'Irony as She Is Cast', 'Jossed', 'Keep Circulating the Tapes', 'Killed by Request', 'Killer App', 'Late Export for You', 'Leslie Nielsen Syndrome', 'Life Imitates Art', 'Real Life', "Limited Special Collector's Ultimate Edition", 'Limey Goes to Hollywood', 'Line to God', 'Loads and Loads of Writers', 'Looping Lines', 'Lying Creator', 'Magnum Opus Dissonance', 'Making Use of the Twin', 'Manual Misprint', 'Marathon Running', 'Marth Debuted in "Smash Bros."', 'McLeaned', 'Meaningful Release Date', 'Meme Acknowledgment', 'Memorial Character', 'The Merch', 'Method Acting', 'Mid-Development Genre Shift', 'Milestone Celebration', 'Missing Episode', 'Missing Trailer Scene', 'Model Dissonance', 'Money, Dear Boy', 'Moved to the Next Console', 'Multiple Languages, Same Voice Actor', 'Mutually Fictional', "Name's the Same", 'Network Death', 'Network to the Rescue', 'Never Work with Children or Animals', 'Newbie Boom', 'No Adaptations Allowed', 'No Budget', 'No Dub for You', 'No Export for You', 'No-Hit Wonder', 'No Port For You', 'No Stunt Double', 'Non-Singing Voice', 'Not Screened for Critics', 'Novelization First', 'Official Fan-Submitted Content', 'Old Shame', 'One-Episode Wonder', 'One for the Money; One for the Art', 'One-Hit Wonder', 'One-Take Wonder', 'Only Barely Renewed', 'Only So Many Canadian Actors', 'Orphaned Reference', "Otaku O'Clock", 'Out of Holiday Episode', 'The Other Darrin', 'The Other Marty', 'The Original Darrin', 'Outlived Its Creator', 'Out of Order', 'Outdated by Canon', 'Overtook the Manga', 'Parody Retcon', 'Paying Their Dues', 'Permanent Placeholder', 'The Pete Best', 'Music', 'Pet Fad Starter', 'Playing Against Type', 'Playing Their Own Twin', 'Playing with Character Type', 'Plays Great Ethnics', 'Pop Culture Urban Legends', 'Popularity Redo', 'Portmanteau Series Nickname', 'Port Overdosed', 'Portrayed by Different Species', 'Posthumous Credit', 'Post-Release Retitle', 'Postscript Season', 'Pre-Order Bonus', 'Preview Piggybacking', 'Produced by Cast Member', 'The Production Curse', 'Production Nickname', 'Fan Nickname', 'Production Posse', 'Promoted Fanboy', 'Prop Recycling', 'Publisher-Chosen Title', 'Queer Character, Queer Actor', 'Queer Show Ghetto', 'Quote Source', 'Reality Subtext', 'Real Life', 'Real-Life Relative', 'Real Life Writes the Hairstyle', 'Real Song Theme Tune', 'Real-Time Timeskip', 'Recast as a Regular', 'Reclusive Artist', 'Recursive Adaptation', 'Recursive Import', 'Recycled Script', 'Recycled Set', 'Recycled: The Series', 'The Red Stapler', 'Referenced by...', 'Refitted for Sequel', 'Relationship Voice Actor', 'Release Date Change', 'Remade for the Export', 'Rereleased for Free', 'Rerun', 'The Resolution Will Not Be Identified', 'Series Finale', 'Revival by Commercialization', 'Role-Ending Misdemeanor', 'Role Reprise', 'Romance on the Set', 'Rule 34 \x96 Creator Reactions', 'Running the Asylum', 'Saved from Development Hell', 'Development Hell', 'Schedule Slip', 'School Study Media', 'Science Marches On', 'Screwed by the Lawyers', 'Screwed by the Merchandise', 'Screwed by the Network', 'Scully Box', 'Self-Adaptation', 'Sequel First', 'Sequel Gap', 'Sending Stuff to Save the Show', 'Separated-at-Birth Casting', 'Sequel in Another Medium', 'Serendipity Writes the Plot', 'Series Hiatus', 'The Shelf of Movie Languishment', 'Shoot the Money', 'Short-Lived Big Impact', 'Short Run in Peru', 'Show Accuracy/Toy Accuracy', 'Shrug of God', 'Similarly Named Works', 'Sleeper Hit', 'So My Kids Can Watch', 'Spared by the Cut', 'Spin-Off Cookbook', 'Spoiled by the Cast List', 'Spoiled by the Merchandise', 'Staff-Created Fan Work', 'Star-Derailing Role', 'Star-Making Role', 'Starring a Star as a Star', 'Stillborn Franchise', 'Film', 'Video Games', 'Streisand Effect', 'Stunt Casting', 'Stunt Double', 'Suppressed Mammaries', 'Surprisingly Lenient Censor', 'Swan Song', '"Take That!" Tit-for-Tat', 'Talking to Himself', 'Teasing Creator', 'Technology Marches On', 'Computers', 'Testing the Editors', 'Those Two Actors', 'Throw It In!', 'Tom Hanks Syndrome', 'Torch the Franchise and Run', 'Trailer Delay', 'Translation Correction', 'Tribute to Fido', 'Trolling Creator', 'Trope Namers', 'Troubled Production', 'Two-Hit Wonder', 'Two Voices, One Character', 'Typecasting', 'Un-Canceled', 'Unbuilt Casting Type', 'Uncredited Role', 'Underage Casting', 'Undermined by Reality', 'Unfinished Dub', 'Unfinished Episode', 'Unintentional Period Piece', 'Unisex Series, Gendered Merchandise', 'Uplifted Side Story', 'Urban Legend of Zelda', 'Vacation, Dear Boy', 'Vaporware', 'Video Source', 'Vindicated by Cable', 'Box Office Bomb', 'Vindicated by Reruns', 'Viral Marketing', 'Voiced Differently in the Dub', 'Voices in One Room', 'Wag the Director', 'What Could Have Been', "Why Fandom Can't Have Nice Things", 'The Wiki Rule', 'Word of Dante', 'Word of Gay', 'Word of God', 'Captain Underpants', 'The Book of Life', 'Word of Saint Paul', 'Working Title', 'Written by Cast Member', 'Writer Conflicts With Canon', 'Word of God', 'Writer Revolt', 'Executive Meddling', 'Write What You Know', 'Write Who You Know', 'Writing by the Seat of Your Pants', 'Written for My Kids', 'Written-In Infirmity', 'You Look Familiar', 'You Might Remember Me from...']}
# {}
# {'Tropes:': ['Narrative Tropes']}
# {'Forgotten Tropes with their own pages': ["30 Minutes, or It's Free!", 'exactly the reason it became such a common comedy trope;', 'A Day in Her Apron', 'Bank Toaster', 'Black Cap of Death', 'Brain Fever', 'Breach of Promise of Marriage', 'Candy Striper', 'The Captivity Narrative', 'The Savage Indian', 'Cheating with the Milkman', 'another visiting laborer', 'Circassian Beauty', 'College Widow', 'Likes Older Women', 'Construction Zone Calamity', 'Divorce in Reno', 'Engagement Challenge', 'Evil Jesuit', 'The Cavalier Years', 'Pedophile Priest', 'Food Pills', 'Dead Unicorn Trope', 'Fourth Reich', 'World War II', 'World War III', 'Argentina Is Nazi-Land', 'Game Show Winnings Cap', "Author's Saving Throw", 'Give the Baby a Father', 'Heroic Russian Émigré', 'defectors in Cold War stories', 'Honorable Marriage Proposal', 'Landline Eavesdropping', 'Technology Marches On', 'Lover and Beloved'], 'Forgotten Tropes without pages': ['Ancient Greece', 'Comedy Tropes', 'Fourth Wall', 'Tropes Are Not Good', 'Undead Horse Tropes', 'absolutely', 'bald-faced', 'Postmodernism', 'is actually', 'Older Than Feudalism', 'Aristotle', 'Samuel Johnson', 'these plays probably did so to keep the scope and budget down', 'Serious Business', 'Four-Temperament Ensemble', 'a debunked medical belief', 'Ancient Egypt', 'temperaments', 'discussed on The Other Wiki', 'which had a reputation for decadence and high living', 'The Golden Ass', 'The Satyricon', 'The Decameron']}
# {'Works by medium:': ['Afghan Media', 'American Media', 'Argentine Media', 'Armenian Media', 'Australian Culture', 'Austrian Media', 'Belarusian Media', 'Belgian Media', 'Brazilian Media', 'British Media', 'Bulgarian Media', 'Canadian Media', 'Chilean Media', 'Chinese Media', 'Colombian Media', 'Croatian Media', 'Cuban Media', 'Czech Media', 'Danish Media', 'Dutch Media', 'Estonian Media', 'Filipino Media', 'Finnish Media', 'French Media', 'Georgian Media', 'German Media', 'Greek Media', 'Hungarian Media', 'Icelandic Media', 'Indonesian Media', 'Indian Media', 'Irish Media', 'Italian Media', 'Israeli Media', 'Jamaican Media', 'Japanese Media', 'Korean Media', 'Latvian Media', 'Malaysian Media', 'Mexican Media', 'Mongolian Media', 'New Zealand Media', 'Nigerian Media', 'Norwegian Media', 'Persian Media', 'Peruvian Media', 'Polish Media', 'Portuguese Media', 'Romanian Media', 'Russian Media', 'Serbian Media', 'Singaporean Media', 'Slovak Media', 'South African Media', 'Spanish Media', 'Swedish Media', 'Swiss Media', 'Taiwanese Media', 'Thai Media', 'Turkish Media', 'Ugandan Media', 'Ukrainian Media', 'Uruguayan Media', 'Venezuelan Media', 'Vietnamese Media']}
# {}
# {}
# {}
# {}
# {'Tropes:': ['Absurdity Ascendant', 'Common Fan Fallacies', 'Continuity Tropes', 'Creator Standpoint Index', 'Deconstruction', 'Doomy Dooms of Doom', 'In-Joke', 'Lit. Class Tropes', 'Metafiction Demanded This Index', 'Fourth Wall', 'Painting the Medium', 'The Newest Ones in the Book', 'The Oldest Ones in the Book', 'The Oldest Tricks in the Book', 'Parody Tropes', 'Self-Demonstrating Article', 'Self-Referential Humor', 'Shout-Out', 'Referenced by...', 'Stock Room', 'The Shades of Fact', 'Trope Tropes']}
# {' Personality Profiles:': ['Five Foundations of Morality', '45 Master Characters', 'Big Five Personality Traits', 'Tabletop Games', 'Dungeons & Dragons', 'Character Alignment', 'Player Archetypes', "The Complete Writer's Guide to Heroes & Heroines", 'The Enneagram', 'Myers-Briggs Temperament Indicator', 'Examples of Myers-Briggs Personalities in Stories', 'Relational Models Theory', 'Systems of Survival'], ' Basic Plots:': ['The 7 Basic Conflicts', 'critics', 'The 7 Basic Plots', 'The Areas of My Expertise', "Asimov's Three Kinds of Science Fiction", "The Author's Ordeal", 'Science Fiction', 'nightmare', 'you', 'Big List of RPG Plots', 'S. John Ross', 'Tabletop RPG', "The Hero's Journey", 'The Hero with a Thousand Faces', 'The Hollywood Formula', 'Master Plots', 'Poetics', 'Aristotle', 'Ur-Example', 'Structural Archetypes', "Propp's Functions of Folktales", 'Ten Movie Plots', 'The Seven Western Plots', 'Story Structure Architect', 'Story: Substance, Structure, Style and The Principles of Screenwriting', 'Understanding Comics'], ' Lists of Clichés:': ['American Cornball', 'The Art of Courtly Love', "Ebert's Glossary of Movie Terms", 'Even a Monkey Can Draw Manga', 'Evil Overlord List', "The Fantasy Novelist's Exam", 'Feminist Frequency', 'Fenimore Coopers Literary Offences', 'The Grand List of Console Role Playing Game Clichés', 'The Grand List of Overused Science Fiction Clichés', 'How NOT to Write a Novel', 'How to Be a Superhero', 'How to Write Badly Well', "Limyaael's Fantasy Rants", 'Poetics', 'Aristotle', 'The RPG Cliches Game', 'Silly Novels by Lady Novelists', 'George Eliot', 'Terrible Writing Advice', 'The Tough Guide to Fantasyland', 'Turkey City Lexicon', 'The Universal Genre Savvy Guide', 'Why Literature Is Bad for You', 'Worst Muse', 'Twitter', 'sarcastically', 'terrible', 'writing practices', 'Cliches'], ' Other works:': ['The American Credo', 'Real Life', 'Blowing Up The Movies', 'Tabletop RPG', 'Danse Macabre', 'Stephen King', 'Horror', 'The Discarded Image', 'C. S. Lewis', 'Earth Is the Center of the Universe', 'All Myths Are True', 'But I Read a Book About It', 'The Fair Folk', 'Fantasy Encyclopedia', 'The Four Loves', 'C. S. Lewis', 'Shipping', "Hamlet's Hit Points", 'Help! My Story Has the Mary-Sue Disease', 'Mary Sue', 'Hieroglyphics', 'Arthur Machen', 'Mechanics, Dynamics, Aesthetics', 'On Fairy-Stories', 'What Does A Martian Look Like'], ' Miscellaneous:': ['Atomic Rockets', 'Bishop Barron', 'The Craft of the Adventure', 'Interactive Fiction', 'Dramatica', 'comic book version', 'Extra Credits', 'The Foundation of S.F. Success', 'Science Fiction', 'Take it with a grain of salt.', 'How to Read Nancy', 'Textual Poachers: Television Fans and Participatory Culture', 'Writing Excuses'], ' Resources without their own pages:': ['The 36 Dramatic Situations', 'The 37 Basic Plots, According to a Screenwriter of the Silent-Film Era', '100 Rules of Anime Physics', 'Aarne-Thompson Classification System', 'Stith Thompson Folk Motif-Index', 'Daily Life Through History Series', 'Useful Notes', 'Hollywood History', "Ebert's Little Movie Glossary", 'The Encyclopedia of Science Fiction', 'The Encyclopedia of Fantasy', "Hero's Journey vs Heroine's Journey", 'here', 'How to Write a Historical Young Adult Novel with an Indian Theme (For Fun and Profit)', 'How to Write about Africa', 'How to Write about Japan', 'The Right Writing', 'The Tough Guide to the Known Galaxy']}
# {'Tropes:': ['Just in Time', 'Probability Tropes', 'Rule of Index', 'Sorting Algorithm of Tropes']}
# {'The list:': ['Doctor Who', 'Star Wars']}
# {' Sub-indexes:': ['Action/Adventure Tropes', 'Advertising Tropes', 'Alternate History Tropes', 'Comedy Tropes', 'Recorded and Stand-Up Comedy', 'Crime and Punishment Tropes', 'Drama Tropes', 'Espionage Tropes', 'Fairy Tale Tropes', 'Game Show Tropes', 'Genre Title Grab Bag', 'Horror Tropes', 'Love Tropes', 'Military and Warfare Tropes', 'Mystery Tropes', 'News Broadcast', 'News Tropes', 'Ninja Tropes', 'Opera', 'Picaresque', 'Pirate Tropes', 'Post-9/11 Terrorism Movie', 'Professional Wrestling', 'Reality TV Tropes', 'Romance Novel Tropes', 'Speculative Fiction Tropes', 'Sports Story Tropes', 'Superhero Tropes', 'Thriller', 'Tragedy', 'Tokusatsu Tropes', 'Wild West Tropes'], ' Tropes related directly to Genres:': ['Contractual Genre Blindness', 'Death by Genre Savviness', 'From Clones to Genre', 'Functional Genre Savvy', 'Gameplay Roulette', 'Genre Adultery', 'Genre Blindness', 'Genre-Busting', 'Genre Deconstruction', 'Genre-Killer', 'Genre Mashup', 'Genre Motif', 'Genre Refugee', 'Genre Relaunch', 'Genre Roulette', 'Genre Savvy', 'Genre Shift', 'Genre Throwback', 'Genre Turning Point', 'Heavy Meta', 'Out-of-Genre Experience', 'Reality Show Genre Blindness', 'Sliding Scale of Comedy and Horror', 'Unexpected Gameplay Change', 'The Universal Genre Savvy Guide', 'Wrong Genre Savvy']}
# {}
# {}
# {}
# {'Related tropes:': ['ANSI Standard Broadcast TV Schedule', 'Adored by the Network', 'Cancellation', 'Channel Hop', 'Executive Meddling', 'Executive Veto', 'International Coproduction', 'Merchandise-Driven', 'Network Death', 'Network Decay', 'Network to the Rescue', 'Niche Network', "Otaku O'Clock", 'Ratings', 'Screwed by the Network', 'State Broadcaster', 'Sports Preemption', 'Syndication', 'Timeshift Channel', '24-Hour News Networks', 'Watershed'], 'Networks Worldwide:': ['ABC', 'TGiF', 'One Saturday Morning and ABC Kids', 'CBS', 'Cookie Jar TV', 'Fox', 'Fox Kids', 'NBC', 'NBC Kids']}
# {'General:': ['Seasons'], 'Technical:': ['3-D Movie', 'Analog vs. Digital', 'Betamax', 'Blu-ray', 'CED', 'Compact Disc', 'DVD', 'DIVX', 'High Definition', 'LaserDisc', 'SD Card', 'VCR', 'U Matic']}
# {}
# {'Tropes and trivia': ['Canon Universe', 'Fan Works', 'Fan Fic', 'Fanfic Tropes', 'Media Adaptation Tropes', 'Adaptation Decay', 'Sequel', 'Translation Tropes']}
# {}
# {'Index of Snowclones:': ['Adverbly Adjective Noun', 'Anime Reality', 'Archaic Weapon for an Advanced Age', 'Elegant Weapon for a More Civilized Age', 'Bizarre Alien Limbs', 'Bizarre Alien Locomotion', 'Bizarre Alien Psychology', 'Bizarre Alien Reproduction', 'Bizarre Alien Senses', 'Bizarre Alien Sexes', 'Bizarre Alien Biology', 'Blood Is Squicker in Water', 'Did You Just Index Cthulhu?', 'Foo Fu', 'Garnishing the Story', 'Good and Evil for Your Convenience', 'Hollywood Style', 'Indexing Ensues', 'Ind ex Machina', 'Infauxmation Desk', 'MacGuffin Snowclones', 'Made of Index', 'No Badge? No Problem!', 'No Plot? No Problem!', 'Our Tropes Are Different', 'The Power of Index', 'Real Award, Fictional Character', 'Real Trailer, Fake Movie', 'Rule of Index', 'Screw This Index, I Have Tropes!', 'Somewhere, This Index Is Crying', 'Suspiciously Similar Song', 'Suspiciously Similar Substitute', 'This Index Will Be Important Later', 'A Troper Is You', 'Tropes on a Bus', 'Tropey the Wonder Dog', 'TV Tropes "How to" Guides', 'We Will Not Use an Index in the Future', "What Do You Mean, It's Not an Index?", 'What Measure Is an Index?', 'Wings Do Nothing', 'Goggles Do Nothing']}
# {}
# {'Tropes:': ['Abandonware', 'Acting in the Dark', 'All There in the Manual', 'All There in the Script', 'Applicability', 'Ascended Fanon', 'Ashcan Copy', 'Avoid the Dreaded G Rating', 'Canon Welding', "Chekhov's Gun", 'Corpsing', 'Creation Myth', 'Creative Differences', 'Cross Through', 'Development Gag', 'Discretion Shot', 'Emotional Torque', 'Enforced Method Acting', 'Fanwork Ban', 'Fights Crime With X', 'First Law of Resurrection', 'Flagship Franchise', 'Front 13, Back 9', 'Fully Absorbed Finale', 'Grand Finale', 'Idiosyncratic Episode Naming', 'Idiosyncratic Wipes', 'I Just Write the Thing', 'Inspiration for the Work', 'Magic Franchise Word', 'Magnum Opus', 'Magnum Opus Dissonance', 'Massive Multiplayer Crossover', 'Method Acting', 'Mythopoeia', 'No Hugging, No Kissing', 'Old Shame', 'One-Episode Wonder', 'Opening Shout-Out', 'Orphaned Reference', 'Parental Bonus', 'Pilot Movie', 'Plot Bunny', 'Poorly Disguised Pilot', 'Production Nickname', 'Reading In', 'Rule of Perception', 'Same Content, Different Rating', "Schrödinger's Gun", 'Shout-Out', 'Simultaneous Arcs', 'Stylistic Suck', 'They Fight Crime!', 'Traveling at the Speed of Plot', 'Troubled Production', 'Villain-Based Franchise', 'World Building', 'Write What You Know', 'Write Who You Know', 'Real Life', 'Writing Around Trademarks', 'Wunza Plot']}
# {'Sub Tropes (as long as they are about the fans themselves, not just what they do):': ['Fan Works']}
# {'Creators by Category:': ['Horror Story Creator Index', 'Mystery Story Creator Index', 'Speculative Fiction Creator Index'], 'Tabletop Game Creators': ['Greg Costikyan', 'Gary Gygax', 'Dungeons & Dragons', 'Kenneth Hite', 'Tabletop Games', 'Ryo Kamiya', 'Robin Laws', 'Feng Shui', 'Phil Masters', 'Tabletop Games', 'Sandy Petersen'], 'Miscellaneous Creators:': ['Agouti-Rex', 'Billy Birmingham', 'Jon Bois', 'Gary Brecher', 'The War Nerd', 'The Chaser', 'Julia Child', 'Chris Crocker', 'Francis E. Dec', 'Mike Duncan', 'End Master', 'Gamebooks', 'Sigmund Freud', 'Hero Of Fire', 'Zelda Classic', 'Zelda Randomizer', 'Carl Jung', 'Kibo', 'Sean Malstrom', 'Mark Musashi', 'Reaver', '4chan', 'Seanbaby', 'Cracked', 'Lore Sjöberg', 'Geek Hierarchy Chart', 'Alexander O. Smith', 'The Weaver', '4chan', 'Ruby Quest', 'Voxus', 'Yuen Woo-Ping', 'The Matrix', 'Kill Bill'], 'Creator Tropes:': ['Actor-Inspired Element', 'Alter-Ego Acting', 'Author Existence Failure', 'Development Hell', 'Authors of Quote', 'Author Usurpation', 'Creator Couple', 'Music', 'Creator Worship', 'Deaf Composer', 'Descended Creator', 'Follow-Up Failure', 'Genre Adultery', 'Lying Creator', 'One-Book Author', 'Pen Name', 'Anonymous Author', 'Moustache de Plume', 'Reclusive Artist', 'Reused Character Design', 'Same Face, Different Name', 'Teasing Creator', 'Trolling Creator', 'Uncredited Role', "Why Fandom Can't Have Nice Things"]}
# {}
# =============================================================================

#these are the pages that seem to require special handling (different structure)
# via handle_special_case:
# =============================================================================
# <DirEntry 'Main Index Index - TV Tropes.htm'>
# <DirEntry 'Home Page _ YMMV - TV Tropes.htm'>
# <DirEntry 'Tropes Of Legend _ Just For Fun - TV Tropes.htm'>
# <DirEntry 'Audience Reactions - TV Tropes.htm'>
# <DirEntry 'The Oldest Ones in the Book - TV Tropes.htm'>
# <DirEntry 'Just For Fun - TV Tropes.htm'>
# <DirEntry 'Information Desk - TV Tropes.htm'>
# <DirEntry 'Contributors - TV Tropes.htm'>
# <DirEntry 'Language Indices - TV Tropes.htm'>
# <DirEntry 'Useful Notes - TV Tropes.htm'>
# <DirEntry 'Genres - TV Tropes.htm'>
# <DirEntry 'Media Tropes - TV Tropes.htm'>
# <DirEntry 'Topical Tropes - TV Tropes.htm'>
# <DirEntry 'Narrative Tropes - TV Tropes.htm'>
# <DirEntry 'Works - TV Tropes.htm'>
# <DirEntry 'Flame Bait - TV Tropes.htm'>
# <DirEntry 'Overdosed Tropes - TV Tropes.htm'>
# =============================================================================

class IndexTree():
    def __init__(self):
        pass
        self.filename = ''
        self.urdict = {}
    def get_lists_tropes(self, filename):
        # this looks like it works for most of the trope list pages, assuming
        # they are similar to each other - i did not check that for all pages this works for,
        # the structure is actually the same as the example page (Indices/Genre Tropes - TV Tropes.htm)
        
        self.filename = filename
        soup = BeautifulSoup(open(filename,encoding="ISO-8859-1"),features="lxml")
        structure_dict = {}
        headerlinks = soup.find_all("h2")
        for headerlink in headerlinks:
            nextul = headerlink.find_next("ul")
            innertropes = nextul.find_all("a")
            innertext = [x.text for x in innertropes]
            structure_dict[headerlink.text]=innertext
        self.urdict = structure_dict
        return structure_dict
    def write_dict(self, dict1):
        try:
            self.newname = self.filename.split("/")[-1]
        except:
            self.newname = self.filename
        self.newname = self.newname.name
        with open("dict_from_"+self.newname+".pickle", 'wb') as outfile:
            pickle.dump(dict1, outfile, protocol=pickle.HIGHEST_PROTOCOL)
        return None
    
    def write_dict_as_string(self, dict1):
        try:
            self.newname = self.filename.split("/")[-1]
        except:
            self.newname = self.filename
        self.newname = self.newname.name
        with open("txt_dict_from_"+self.newname+".txt","w") as outfile:
            outfile.write(str(dict1))
        return None
        
    def get_df(self):
        self.dictdf = pd.DataFrame.from_dict(self.urdict)
        
    def get_lists_tropes_df(self, filename):
        # doesn't work i think?
        self.pdobject = pd.read_html(filename, encoding='latin-1')
        return self.pdobject
            
    def go_thru_list_pages(self,foldername):
        for entry in os.scandir(foldername):
            if entry.path.endswith(".htm"):
                dict1 = self.get_lists_tropes(entry)
                if dict1 == {}:
                    dict1 = self.handle_special_cases_flatly(entry)
                else:
                    pass
                self.write_dict(dict1)
                self.write_dict_as_string(dict1)
            else: pass
        return None
    
    def handle_special_cases_flatly(self, filename):
        structure_dict = {}
        self.filename = filename
        soup = BeautifulSoup(open(filename,encoding="ISO-8859-1"),features="lxml")
        #<div id="main-article" class="article-content retro-folders">
        mydivs = soup.find_all("div", class_="article-content retro-folders")
        if len(mydivs) == 0:
            #print("different structure: ",filename)
            #there seems to be one more special case, 'Main Index Index - TV Tropes.htm'
            self.handle_main_index(filename)
        else:
            for div in mydivs:
                nextul = div.find_next("ul")
                innertropes = nextul.find_all("a")
                innertext = [x.text for x in innertropes]
                structure_dict[div.text] = innertext
        return structure_dict
    
    def handle_main_index(self, filename):
        structure_dict = {}
        self.filename = filename
        soup = BeautifulSoup(open(filename,encoding="ISO-8859-1"),features="lxml")
        mydivs = soup.find_all("div", class_="article-content")
        if len(mydivs) == 0:
            print("oh no")
            return None
        else:
            for div in mydivs:
                mycategories = div.find_all("div", class_="legend")
                for category in mycategories:
                    mylinks = category.find_next("div", class_="link-set")
                    myas = mylinks.find_all("a")
                    linktext = [x.text for x in myas]
                    structure_dict[category.text] = linktext
        #print(structure_dict)
        return structure_dict
                
        

it = IndexTree()
#print(it.get_lists_tropes("Indices/Genre Tropes - TV Tropes.htm"))
#it.write_dict()
it.go_thru_list_pages("Indices")
    