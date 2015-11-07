def mail_score(name, mail):
    score = 1
    name = str(name).lower().replace('-', ' ')
    mail_name = str(mail).lower().split('@')[0]
    names = name.split(' ')
    for subname in names:
        if subname in mail_name:
            score += 2 * len(subname)
        else:
            if subname[0] in mail_name:
                score += 1
    return score


if __name__ == '__main__':
    name = 'Rigori Fursin'
    mail = 'grigori.fursin@ctuning.org'
    print mail_score(name, mail)