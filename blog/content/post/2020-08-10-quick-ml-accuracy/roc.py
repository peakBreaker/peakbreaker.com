import matplotlib.pyplot as plt  # doctest: +SKIP
from sklearn import datasets, metrics, model_selection, svm
X, y = datasets.make_classification(random_state=0)
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, random_state=0)
clf = svm.SVC(random_state=0)
clf.fit(X_train, y_train)
svm.SVC(random_state=0)
metrics.plot_roc_curve(clf, X_test, y_test)  # doctest: +SKIP
plt.title('ROC Curve for simple SVM')
plt.show()                                   # doctest: +SKIP
