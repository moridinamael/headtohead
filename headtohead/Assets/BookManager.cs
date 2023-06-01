using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

public class BookManager : MonoBehaviour
{
    public GameObject bookPrefab;
    public RectTransform bookParent;
    public Text matchupText;

    private List<Book> books;
    private Book book1;
    private Book book2;

    private void Start()
    {
        books = new List<Book>();

        for (int i = 0; i < 2; i++)
        {
            var book = new GameObject($"Book{i + 1}").AddComponent<Book>();
            book.Initialize($"Book{i + 1}", bookParent, i);
            books.Add(book);
        }

        SetupNextMatchup();
    }

    public void OnBookSelected(Book selectedBook)
    {
        Debug.Log("Book selected: " + selectedBook.Title);
        string outcome = selectedBook == book1 ? "1" : "2";

        book1.UpdateRating(book2, outcome);
        book2.UpdateRating(book1, outcome == "1" ? "2" : "1");

        UpdateBookPosition(book1);
        UpdateBookPosition(book2);

        SetupNextMatchup();
    }

    private void DisplayMatchup(Book book1, Book book2)
    {
        matchupText.text = $"1. {book1.Title}\n2. {book2.Title}";
    }

    private void SetupNextMatchup()
    {
        book1 = books[Random.Range(0, books.Count)];
        do
        {
            book2 = books[Random.Range(0, books.Count)];
        } while (book1 == book2);

        DisplayMatchup(book1, book2);
    }

    private void UpdateBookPosition(Book book)
    {
        float yPos = (book.Rating / 800) * bookParent.rect.height;  // assuming 800 is the max rating
        book.transform.localPosition = new Vector3(book.transform.localPosition.x, yPos, book.transform.localPosition.z);
    }
}
