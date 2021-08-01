import json
import re

from collections import Counter
from conf import df

# Text from answers on the question: What associations come to your mind when you hear the term 'food waste'?

df = df[['date', 'assoc']].copy().dropna()

# Stopwords

stopwords = set("i,me,my,myself,we,us,our,ours,ourselves,you,your,yours,yourself,yourselves,he,him,his,himself,she,her,hers,herself,it,its,itself,they,them,their,theirs,themselves,what,which,who,whom,whose,this,that,these,those,am,is,are,was,were,be,been,being,have,has,had,having,do,does,did,doing,will,would,should,can,could,ought,i'm,you're,he's,she's,it's,we're,they're,i've,you've,we've,they've,i'd,you'd,he'd,she'd,we'd,they'd,i'll,you'll,he'll,she'll,we'll,they'll,isn't,aren't,wasn't,weren't,hasn't,haven't,hadn't,doesn't,don't,didn't,won't,wouldn't,shan't,shouldn't,can't,cannot,couldn't,mustn't,let's,that's,who's,what's,here's,there's,when's,where's,why's,how's,a,an,the,and,but,if,or,because,as,until,while,of,at,by,for,with,about,against,between,into,through,during,before,after,above,below,to,from,up,upon,down,in,out,on,off,over,under,again,further,then,once,here,there,when,where,why,how,all,any,both,each,few,more,most,other,some,such,no,nor,not,only,own,same,so,than,too,very,say,says,said,shall,and,that,are,you,your,goes,которую".split(','))

exclusive = ['too good to go', 'climate change', 'net zero', 'throwing away', 'hard work', 'people in need', 'use-by date']

color_food  = '#0a9396'
color_waste = '#e5989b'
color_money = '#ffb703'
color_olio  = '#81b29a'
color_other = '#999'

colors = {
    'food': color_food, 'waste': color_food, 'meal': color_food, 'groccery': color_food, 'grocery': color_food, 'еда': color_food,
    'change': color_waste, 'landfills': color_waste, 'garbage': color_waste, 'environment': color_waste,  'planet': color_waste, 'world': color_waste, 'wasted': color_waste, 'wasting': color_waste, 'trash': color_waste,
    'too good to go': color_olio, 'olio': color_olio, 'compost': color_olio, 'supermarkets': color_olio, 'магазины': color_olio, 'stores': color_olio,
    'hungry': color_money, 'poverty': color_money, 'money': color_money, 'денег':color_money, 'consumerism': color_money
}

# Words from Reddit post

reddit = [
    'Children',
    'A thing my college dining hall loved to guilt trip us about',
    'Bakeries/grocery stores, I use to work at a bakery located in a grocery store and they use to over produce so much that would be thrown out the next day, what’s worse is the fact that the food can’t be donated',
'Edible underpants',
    'Restaurants, grocery stores, rotting veggies',
    'BFI, WM.',
    'Eating only a portion of something then throwing it away.',
    'The government',
    'The United States of America, they who destroyed the world with their fast-food industry.',
    'Garbage disposal'
]

# Exclusive search for specific words

text = ' '.join(df.assoc.tolist() + reddit).lower()

count = Counter()

for e in exclusive:
    c = text.count(e)

    if c > 0:
        count[e] = c
        text = text.replace(e, ' ')

# All other words

words = filter(
            lambda x: x not in stopwords and len(x) > 1,
            re.sub('[\W\_]+', ' ', text).split()
        )

count.update(words)

# Word Cloud data structure

word_cloud = [{'text': w, 'size': c, 'color': colors.get(w) or '#999'} for w, c in count.items() if c > 1]


# Output

if __name__ == '__main__':
    with open('output/word_cloud.js', 'w', encoding='utf-8') as f:
        f.write('var word_cloud =\n' + json.dumps(word_cloud, ensure_ascii=False) + ';\n')