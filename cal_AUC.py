#!/usr/bin/env python
# coding=utf-8

import sys

def main():
    if 3 > len(sys.argv):
        sys.stderr.write('usage: ' + sys.argv[0] + ' predict_col reward_col\n')
        sys.stderr.write('   e.g.: ' + sys.argv[0] + ' 0 2\n')
        return -1

    MAX_SPLIT = 10000
    predict_col = int(sys.argv[1])
    reward_col = int(sys.argv[2])
    min_col = max(predict_col, reward_col)

    pos_count = [0 for i in range(MAX_SPLIT + 1)]
    neg_count = [0 for i in range(MAX_SPLIT + 1)]

    line_count = 0
    total_pos_count = 0
    for line in sys.stdin:
        terms = line.strip().split("\t")
        if len(terms) > min_col:
            line_count += 1
            pre_val = min(1.0, max(0.0, float(terms[predict_col])))
            rew_val = terms[reward_col]
            index  = int(pre_val * MAX_SPLIT)
            if  float(rew_val) != 0.0:
                total_pos_count += 1
                pos_count[index] += 1
            else:
                neg_count[index] += 1

    auc = 0.0
    last_tpr = 1
    last_fpr = 1
    for threshold in range(MAX_SPLIT):
        tp = 0
        fn = 0
        fp = 0
        tn = 0
        tpr = 0.0
        fpr = 0.0
        for i in range(threshold):
            fn += pos_count[i]
            tn += neg_count[i]
        for i in range(threshold, MAX_SPLIT + 1):
            tp += pos_count[i]
            fp += neg_count[i]
        if tp + fn != 0:
            tpr = float(tp) / float(tp + fn)
        if fp + tn != 0:
            fpr = float(fp) / float(fp + tn)

        #print str(tpr) + "\t" + str(fpr)
        auc += (last_tpr + tpr) / 2 * (last_fpr - fpr)
        last_tpr = tpr
        last_fpr = fpr
    print "line_count:", line_count
    print "pos_count:", total_pos_count
    print "auc:", auc

if __name__ == "__main__":
    main()
