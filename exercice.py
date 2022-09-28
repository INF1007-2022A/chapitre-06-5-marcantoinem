#!/usr/bin/env python
# -*- coding: utf-8 -*-


def check_brackets(text, brackets):
	to_close = [""]
	opener = dict(zip(brackets[0::2], brackets[1::2]))
	for char in text:
		if char in opener:
			to_close.append(char)
		elif opener[to_close[-1]] == char:
			to_close.pop()
	return to_close == [""]

def remove_comments(full_text, comment_start, comment_end):
	comments_to_remove = []
	in_comment = False
	error = False
	for i in range(len(full_text)):
		if full_text[i:i+len(comment_start)] == comment_start and not in_comment:
			to_remove_start = i
			in_comment = True
		elif full_text[i:i+len(comment_start)] == comment_start and in_comment:
			error = True
		elif full_text[i:i+len(comment_end)] == comment_end and in_comment:
			to_remove_end = i
			comments_to_remove.append((to_remove_start,to_remove_end))
			in_comment = False
		elif full_text[i:i+len(comment_end)] == comment_end and not in_comment:
			error = True
	
	if error or in_comment:
		full_text = None
	elif comments_to_remove != []:
		for start, end in comments_to_remove[::-1]:
			full_text = full_text[:start] + full_text[end+2:]

	return full_text

def get_tag_prefix(text, opening_tags, closing_tags):
	for opening_tag in opening_tags:
		if text[0:len(opening_tag)] == opening_tag:
			return (opening_tag, None)
	for closing_tag in closing_tags:
		if text[0:len(closing_tag)] == closing_tag:
			return (None, closing_tag)
	return (None, None)

def check_tags(full_text, tag_names, comment_tags):
	to_close = [""]
	full_text = remove_comments(full_text, "<!--", "-->")
	if full_text == None:
		return False
	for i in range(len(full_text)):
		if full_text[i] == "<":
			if full_text[i+1] == "/":
					if full_text[i+2:i+len(to_close[-1])+3] == to_close[-1] + ">":
						to_close.pop()
					else:
						return False
			for tag_name in tag_names:
				if full_text[i+1:i+len(tag_name)+2] == tag_name + ">":
					to_close.append(tag_name)
	return to_close == [""]



if __name__ == "__main__":
	brackets = ("(", ")", "{", "}")
	yeet = "(yeet){yeet}"
	yeeet = "({yeet})"
	yeeeet = "({yeet)}"
	yeeeeet = "(yeet"
	print(check_brackets(yeet, brackets))
	print(check_brackets(yeeet, brackets))
	print(check_brackets(yeeeet, brackets))
	print(check_brackets(yeeeeet, brackets))
	print()

	spam = "Hello, /* OOGAH BOOGAH */world!"
	eggs = "Hello, /* OOGAH BOOGAH world!"
	parrot = "Hello, OOGAH BOOGAH*/ world!"
	print(remove_comments(spam, "/*", "*/"))
	print(remove_comments(eggs, "/*", "*/"))
	print(remove_comments(parrot, "/*", "*/"))
	print()

	otags = ("<head>", "<body>", "<h1>")
	ctags = ("</head>", "</body>", "</h1>")
	print(get_tag_prefix("<body><h1>Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("<h1>Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("</h1></body>", otags, ctags))
	print(get_tag_prefix("</body>", otags, ctags))
	print()

	spam = (
		"<html>"
		"  <head>"
		"    <title>"
		"      <!-- Ici j'ai écrit qqch -->"
		"      Example"
		"    </title>"
		"  </head>"
		"  <body>"
		"    <h1>Hello, world</h1>"
		"    <!-- Les tags vides sont ignorés -->"
		"    <br>"
		"    <h1/>"
		"  </body>"
		"</html>"
	)
	eggs = (
		"<html>"
		"  <head>"
		"    <title>"
		"      <!-- Ici j'ai écrit qqch -->"
		"      Example"
		"    <!-- Il manque un end tag"
		"    </title>-->"
		"  </head>"
		"</html>"
	)
	parrot = (
		"<html>"
		"  <head>"
		"    <title>"
		"      Commentaire mal formé -->"
		"      Example"
		"    </title>"
		"  </head>"
		"</html>"
	)
	tags = ("html", "head", "title", "body", "h1")
	comment_tags = ("<!--", "-->")
	print(check_tags(spam, tags, comment_tags))
	print(check_tags(eggs, tags, comment_tags))
	print(check_tags(parrot, tags, comment_tags))
	print()

