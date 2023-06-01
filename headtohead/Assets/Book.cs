using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

public class Book : MonoBehaviour, IPointerClickHandler
{
    public string Title { get; private set; }
    public float Rating { get; private set; }
    public Button ButtonObject { get; private set; }  // Add this line
    private const float K = 32;
    
    public void Initialize(string title, RectTransform parentTransform, int index)
    {
        Title = title;
        Rating = 400;
        //Create Button GameObject and attach Button component
        GameObject buttonObject = new GameObject(title);
        ButtonObject = buttonObject.AddComponent<Button>();
        ButtonObject.transform.SetParent(parentTransform, false);
        //Attach Text component to Button and set its properties
        Text buttonText = ButtonObject.gameObject.AddComponent<Text>();
        buttonText.text = title;
        buttonText.alignment = TextAnchor.MiddleCenter;
        //Set the button's RectTransform to fill its parent
        RectTransform buttonRect = ButtonObject.GetComponent<RectTransform>();
        buttonRect.anchorMin = new Vector2(0, 0);
        buttonRect.anchorMax = new Vector2(1, 1);
        buttonRect.anchoredPosition = new Vector2(0, -50 * index);
        buttonRect.sizeDelta = new Vector2(100, 30);

        ButtonObject.onClick.AddListener(() => FindObjectOfType<BookManager>().OnBookSelected(this));
    }


    public void OnPointerClick(PointerEventData eventData)
    {
        Debug.Log("Book clicked: " + Title);
        FindObjectOfType<BookManager>().OnBookSelected(this);
    }

    public void UpdateRating(Book opponent, string outcome)
    {
        Rating = CalculateElo(Rating, opponent.Rating, outcome);
        opponent.Rating = CalculateElo(opponent.Rating, Rating, outcome == "1" ? "2" : "1");
    }

    private float CalculateElo(float rating1, float rating2, string outcome)
    {
        float R1 = Mathf.Pow(10, rating1 / 400);
        float R2 = Mathf.Pow(10, rating2 / 400);

        float E1 = R1 / (R1 + R2);
        float S1 = outcome == "1" ? 1 : 0;

        return rating1 + K * (S1 - E1);
    }
}