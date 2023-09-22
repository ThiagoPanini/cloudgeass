# Frequently Asked Questions

Here we will found some common questions about *cloudgeass*. Of course we provided the answers too 🤣

??? question "Why use cloudgeass and we already have boto3?"
    That's a good question and the answear for it is straitghforward: the *cloudgeass* python package just put together some client and resource methods from boto3 in order to delivery an easier interface for users that want to do specific tasks in AWS.

    You can always choose to use boto3's source methods instead, but think about a way to create a single function or a single method that applies some specific rules and blocks of code using multiple boto3 methods. That is *cloudgeass*!


??? question "I have something in my mind to collaborate with the iniciative. How can I proceed?"
    Excellent! It's always nice to have new contributors. For everyone interested in joining the contributors team, check the [contributing](../contributing/contributing.md) page for more details.

    Just as an additional comment, it's extremelly important to check the [library structure](../library-structure.md) page to see how *cloudgeass* is structured and organized within its methods and classes. That could give future contributors a good idea how to put their code here.