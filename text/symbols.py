""" from https://github.com/keithito/tacotron """

"""
Defines the set of symbols used in text input to the model.
-- uses IPA phonemes only
-- IPA datas from https://github.com/AdamSteffanick/ipa-data/blob/master/guid-o-matic/ipa-data/ipa-data.csv
"""
_pad = "<pad>"
_punctuation = ";:,.!?¡¿—…\"«»“” "
_ipa_symbols = "!!	(	((	(.)	(..)	(...)	)	))	*	/	1	2	3	A	B	C	C	D	E	F	F	G	H	I	J	J	K	L	L	M	N	O	P	Q	R	S	T	U	V	V	W	W	X	Y	Z	[	\	]	a	b	c	d	e	f	g	h	i	j	k	l	m	n	o	p	q	r	s	t	u	v	w	x	y	z	{	|	}	æ	ç	ð	ø	č	ħ	ı	ŋ	Œ	œ	š	ž	ƈ	ƙ	ƛ	ƞ	ƥ	ƫ	ƭ	ƻ	ǀ	ǁ	ǂ	ǃ	ǰ	ȡ	ȵ	ȶ	ɐ	ɑ	ɒ	ɓ	ɔ	ɕ	ɖ	ɗ	ɘ	ə	ɚ	ɛ	ɜ	ɞ	ɟ	ɠ	ɡ	ɢ	ɣ	ɤ	ɥ	ɦ	ɧ	ɨ	ɩ	ɪ	ɫ	ɬ	ɭ	ɮ	ɯ	ɰ	ɱ	ɲ	ɳ	ɴ	ɵ	ɶ	ɷ	ɸ	ɹ	ɺ	ɻ	ɼ	ɽ	ɾ	ʀ	ʁ	ʂ	ʃ	ʄ	ʆ	ʇ	ʈ	ʉ	ʊ	ʋ	ʌ	ʍ	ʎ	ʏ	ʐ	ʑ	ʒ	ʓ	ʔ	ʕ	ʖ	ʗ	ʘ	ʙ	ʚ	ʛ	ʜ	ʝ	ʞ	ʟ	ʠ	ʡ	ʢ	ʣ	ʤ	ʥ	ʦ	ʧ	ʨ	ʩ	ʪ	ʫ	ʭ	ʰ	ʰ	ʲ	ʶ	ʷ	ʸ	ʻ	ʼ	ˆ	ˇ	ˈ	ˌ	ː	ˑ	˖	˗	˞	ˠ	ˡ	ˢ	ˣ	ˤ	˥	˥˩	˦	˦˥	˧	˧˦˧	˨	˩	˩˥	˩˨	ˬ	ˬ	˭	˱	˲	˷	˹	̀	́	̂	̃	̄	̆	̇	̈	̋	̌	̏	̑	̖;ˎ	̗;ˏ	̘	̙	̚	̜	̝;˔	̞;˕	̟	̠	̡	̢	̣	̤	̥;̊	̥₎	̩	̪	̫	̬	̬₎	̯	̰	̴	̹	̺	̻	̼	̽	͆	̪͆	͇	͈	͉	͊	͋	͌	͍	͎	͡	͢	Θ	β	θ	λ	χ	ᵊ	ᶑ	ᶹ	ᶿ	᷄	᷅	᷈	‖	‿	ⁿ	₍̥	₍̥₎	₍̬	₍̬₎	↑	↑	↓	↓	↗	↘	❍	ⱱ	ꟸ	ꟹ	𝆏	𝆏𝆏	𝆑	𝆑𝆑	𝑎𝑙𝑙𝑒𝑔𝑟𝑜	𝑙𝑒𝑛𝑡𝑜"
# Export all symbols:
symbols = [_pad] + _ipa_symbols.split("\t") + list(_punctuation) + ["<bos>", "<eos>", "<space>"]

# Special symbol ids
SPACE_ID = symbols.index("<space>")

#print(symbols)
